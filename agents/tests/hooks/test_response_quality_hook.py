#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import io
import json
import socket
import subprocess
import sys
import unittest
import urllib.error
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[3]
PLUGIN_ROOT = REPO_ROOT / "plugins/codewizard"
HOOKS_JSON = PLUGIN_ROOT / "hooks/hooks.json"
GUARD_SCRIPT = PLUGIN_ROOT / "hooks/guard_response.py"


def load_guard_module():
    spec = importlib.util.spec_from_file_location("guard_response", GUARD_SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


guard = load_guard_module()


class ResponseQualityHookTest(unittest.TestCase):
    def test_stop_hook_is_registered(self) -> None:
        hooks = json.loads(HOOKS_JSON.read_text(encoding="utf-8"))["hooks"]
        commands = [hook["command"] for group in hooks["Stop"] for hook in group["hooks"]]
        self.assertEqual(commands, ['python3 "$PLUGIN_ROOT/hooks/guard_response.py"'])

    def test_word_limit_allows_500_and_blocks_501(self) -> None:
        allowed = guard.validate_response("word " * 500)
        blocked = guard.validate_response("word " * 501)
        self.assertEqual(allowed, [])
        self.assertIn("501 words", "\n".join(blocked))

    def test_keywords_are_complete_words_and_ignore_code(self) -> None:
        response = "Notification differs. `if unknown`\n```python\nif unclear:\n    pass\n```"
        allowed = guard.validate_response(response)
        blocked = guard.validate_response("IFS, RECOMMENDATIONS, unknowns, caveats, and unclears.")
        self.assertEqual(allowed, [])
        prompt = "\n".join(blocked)
        self.assertIn("Do not teach the user what to do; do it yourself", prompt)
        self.assertIn("unknowns, caveats, unclears", prompt)
        self.assertIn("Have you exhausted all available information", prompt)
        self.assertIn("No if-based speculation", prompt)

    def test_reports_every_broken_link_at_once(self) -> None:
        failures = {
            "https://missing.example/a": "HTTP 404",
            "https://gone.example/b": "HTTP 410",
        }
        response = "See https://missing.example/a and [gone](https://gone.example/b)."
        with patch.object(guard, "check_url", side_effect=failures.get):
            result = guard.validate_response(response)
        prompt = "\n".join(result)
        self.assertIn("https://missing.example/a (HTTP 404)", prompt)
        self.assertIn("https://gone.example/b (HTTP 410)", prompt)

    def test_urls_inside_code_are_not_treated_as_links(self) -> None:
        response = "`https://inline.invalid`\n```text\nhttps://fenced.invalid\n```"
        result = guard.validate_response(response)
        self.assertEqual(result, [])

    def test_http_404_blocks_but_access_denial_and_temporary_errors_pass(self) -> None:
        addresses = [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443))]

        def resolver(*args, **kwargs):
            return addresses

        def http_error(code):
            def opener(request, timeout):
                raise urllib.error.HTTPError(request.full_url, code, "status", {}, None)

            return opener

        with patch.object(guard.socket, "getaddrinfo", side_effect=resolver):
            with patch.object(guard.urllib.request, "urlopen", side_effect=http_error(404)):
                self.assertEqual(guard.check_url("https://example.com/missing"), "HTTP 404")
            with patch.object(guard.urllib.request, "urlopen", side_effect=http_error(403)):
                self.assertEqual(guard.check_url("https://example.com/private"), "")
            with patch.object(guard.urllib.request, "urlopen", side_effect=http_error(503)):
                self.assertEqual(guard.check_url("https://example.com/error"), "")

        def temporary_error(request, timeout):
            raise urllib.error.URLError(TimeoutError("timed out"))

        with patch.object(guard.socket, "getaddrinfo", side_effect=resolver):
            with patch.object(guard.urllib.request, "urlopen", side_effect=temporary_error):
                self.assertEqual(guard.check_url("https://example.com/slow"), "")

    def test_nxdomain_blocks_but_temporary_dns_failure_passes(self) -> None:
        def nxdomain(*args, **kwargs):
            raise socket.gaierror(socket.EAI_NONAME, "name not known")

        def temporary(*args, **kwargs):
            raise socket.gaierror(socket.EAI_AGAIN, "try again")

        with patch.object(guard.socket, "getaddrinfo", side_effect=nxdomain):
            self.assertEqual(
                guard.check_url("https://missing.invalid/path"),
                "domain does not exist",
            )
        with patch.object(guard.socket, "getaddrinfo", side_effect=temporary):
            self.assertEqual(guard.check_url("https://temporary.example/path"), "")

    def test_first_failure_blocks_and_repeated_failure_terminates_loop(self) -> None:
        payload = {"last_assistant_message": "This has an unclear caveat.", "stop_hook_active": False}
        first = self.run_main(payload)
        self.assertEqual(first["decision"], "block")

        payload["stop_hook_active"] = True
        repeated = self.run_main(payload)
        self.assertNotIn("decision", repeated)
        self.assertIn("allowed the turn after one correction attempt", repeated["systemMessage"])

    def test_command_entrypoint_returns_valid_stop_json(self) -> None:
        payload = {"last_assistant_message": "This is unclear.", "stop_hook_active": False}
        result = subprocess.run(
            [sys.executable, str(GUARD_SCRIPT)],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["decision"], "block")

    def run_main(self, payload: dict) -> dict:
        output = io.StringIO()
        with patch.object(sys, "stdin", io.StringIO(json.dumps(payload))), redirect_stdout(output):
            self.assertEqual(guard.main(), 0)
        return json.loads(output.getvalue())


if __name__ == "__main__":
    unittest.main()
