#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import textwrap
import unittest
import importlib.util
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
PLUGIN_ROOT = REPO_ROOT / "plugins/codewizard"
PLUGIN_JSON = REPO_ROOT / "plugins/codewizard/.codex-plugin/plugin.json"
HOOKS_JSON = REPO_ROOT / "plugins/codewizard/hooks/hooks.json"
GUARD_SCRIPT = REPO_ROOT / "plugins/codewizard/hooks/guard_mission_brief.py"


def load_guard_module():
    spec = importlib.util.spec_from_file_location("guard_mission_brief", GUARD_SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def brief(status: str = "Pending", extra_section: str = "", omit_clarification: bool = False) -> str:
    text = textwrap.dedent(
        f"""\
        # Mission Brief: Add Sample Behavior

        ## Initial User Request

        Add sample behavior.

        ## Formal Requirements

        | Requirement | Definition of Done (DoD) | Test Plan | Result |
        |---|---|---|---|
        | Add sample behavior | `sample` returns `ok`. | Run `sample --check`. | Pending |

        ## Approval Status
        {status}

        ## Mission Status
        Pending. Filled when the mission is complete.

        ## Clarification

        ### Clarification Tree
        - Question: What should the sample command return?
          - Answer: It should return `ok`.
          - Updated understanding: The mission is to make `sample --check` return `ok`.
          - Follow-ups:
            - Question: Should the behavior apply only to `sample --check`?
              - Answer: Yes.
              - Updated understanding: Other sample command behavior is outside the mission.
              - Follow-ups: none
            - Question: Should existing error behavior change?
              - Answer: No.
              - Updated understanding: Existing error behavior must remain unchanged.
              - Follow-ups: none
        - Question: Should the output include a trailing newline?
          - Answer: No.
          - Updated understanding: The command must print exactly `ok`.
          - Follow-ups: none

        ### Clarified Intent
        Make the sample check return `ok`.

        ## User Feedback

        - Round 1: Approved.
        """
    )
    if omit_clarification:
        start = text.index("\n## Clarification\n")
        end = text.index("\n## User Feedback\n")
        text = text[:start] + text[end:]
    return text + extra_section


def hook_commands(event: str) -> list[str]:
    hooks = json.loads(HOOKS_JSON.read_text(encoding="utf-8"))["hooks"][event]
    commands: list[str] = []
    for group in hooks:
        commands.extend(hook["command"] for hook in group["hooks"])
    return commands


class CodeMissionHooksTest(unittest.TestCase):
    def run_hook_command(
        self, command: str, payload: dict, mission_dir: Path, cwd: Path = REPO_ROOT
    ) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["CODE_MISSION_DIR"] = str(mission_dir)
        env["PLUGIN_ROOT"] = str(PLUGIN_ROOT)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            command,
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            cwd=str(cwd),
            env=env,
            shell=True,
            check=False,
        )

    def run_event(
        self, event: str, payload: dict, mission_dir: Path, cwd: Path = REPO_ROOT
    ) -> list[subprocess.CompletedProcess[str]]:
        return [self.run_hook_command(command, payload, mission_dir, cwd) for command in hook_commands(event)]

    def test_hooks_json_has_pre_and_post_tool_mission_file_commands(self) -> None:
        plugin = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))
        self.assertEqual(plugin["hooks"], "./hooks/hooks.json")

        hooks = json.loads(HOOKS_JSON.read_text(encoding="utf-8"))["hooks"]
        pre = hook_commands("PreToolUse")
        post = hook_commands("PostToolUse")
        self.assertEqual(
            pre,
            ['python3 "$PLUGIN_ROOT/hooks/guard_mission_identity.py"'],
        )
        self.assertEqual(
            post,
            ['python3 "$PLUGIN_ROOT/hooks/guard_mission_brief.py"'],
        )

    def test_every_failure_code_has_specific_recovery_action(self) -> None:
        guard = load_guard_module()
        failure_codes = {
            "approval_status",
            "clarification_sections",
            "clarification_tree",
            "formal_requirements",
            "missing_clarification",
            "title",
            "top_sections",
            "unresolved_clarification",
            "unreadable",
        }
        self.assertEqual(set(guard.ACTION_BY_FAILURE_CODE), failure_codes)
        actions = guard.recovery_actions([guard.Failure(code, code) for code in sorted(failure_codes)])
        self.assertEqual(len(actions), len(set(actions)))
        self.assertNotIn("Repair the listed mission brief failures, then rerun the write.", actions)

    def test_post_tool_reports_all_mission_brief_failures(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            mission_dir = Path(tmp) / "missions"
            mission_dir.mkdir()
            mission_path = mission_dir / "brief.md"
            bad_brief = textwrap.dedent(
                """\
                # Mission Brief

                ## Initial User Request

                Add sample behavior.

                ## Formal Requirements

                No table here.

                ## Approval Status
                Maybe

                ## Mission Status
                Pending.

                ## User Feedback

                - Round 1: Needs work.

                ## Explanation

                Extra section.
                """
            )
            mission_path.write_text(bad_brief, encoding="utf-8")
            payload = {
                "hook_event_name": "PostToolUse",
                "tool_name": "Write",
                "tool_input": {"file_path": str(mission_path)},
            }
            results = self.run_event("PostToolUse", payload, mission_dir)
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0].returncode, 2, results[0].stderr)
            self.assertIn("Next action:", results[0].stderr)
            self.assertIn("Start the code-mission clarification process with the user before creating or revising the mission brief.", results[0].stderr)
            self.assertIn("Rewrite the mission brief to match the template exactly; remove sections not defined by the template.", results[0].stderr)
            self.assertIn("Set a valid Approval Status based on the current situation. Zero tolerance for forging the user's approval", results[0].stderr)
            self.assertNotIn("Set Approval Status to Pending unless", results[0].stderr)
            self.assertIn("Repair Formal Requirements as a table with Requirement and Result columns.", results[0].stderr)
            self.assertIn("Change the title to '# Mission Brief: <short title>'.", results[0].stderr)
            self.assertNotIn("Do not continue implementation or edit project files.", results[0].stderr)
            self.assertIn("Refer to the code-mission skill instructions for the required mission brief format and approval rules.", results[0].stderr)
            self.assertIn("Failures:", results[0].stderr)
            self.assertIn("mission brief must start with '# Mission Brief: <short title>'", results[0].stderr)
            self.assertIn("mission brief sections must exactly be", results[0].stderr)
            self.assertIn("missing ## Clarification section", results[0].stderr)
            self.assertIn("Approval Status must be exactly Pending, Approved, or Rejected", results[0].stderr)
            self.assertIn("Formal Requirements must be a table with Requirement and Result columns", results[0].stderr)

    def test_post_tool_allows_valid_mission_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            mission_dir = Path(tmp) / "missions"
            mission_dir.mkdir()
            mission_path = mission_dir / "brief.md"
            mission_path.write_text(brief("Pending"), encoding="utf-8")
            payload = {
                "hook_event_name": "PostToolUse",
                "tool_name": "Write",
                "tool_input": {"file_path": str(mission_path)},
            }
            results = self.run_event("PostToolUse", payload, mission_dir)
            self.assertEqual([result.returncode for result in results], [0], [result.stderr for result in results])

    def test_post_tool_extra_section_action_removes_undefined_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            mission_dir = Path(tmp) / "missions"
            mission_dir.mkdir()
            mission_path = mission_dir / "brief.md"
            mission_path.write_text(brief(extra_section="\n## Explanation\n\nExtra text.\n"), encoding="utf-8")
            payload = {
                "hook_event_name": "PostToolUse",
                "tool_name": "Write",
                "tool_input": {"file_path": str(mission_path)},
            }
            results = self.run_event("PostToolUse", payload, mission_dir)
            self.assertEqual(results[0].returncode, 2, results[0].stderr)
            self.assertIn("Rewrite the mission brief to match the template exactly; remove sections not defined by the template.", results[0].stderr)
            self.assertNotIn("Start the code-mission clarification process", results[0].stderr)

    def test_post_tool_command_works_from_project_cwd(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mission_dir = root / "missions"
            project_dir = root / "project"
            mission_dir.mkdir()
            project_dir.mkdir()
            mission_path = mission_dir / "brief.md"
            mission_path.write_text(brief(omit_clarification=True), encoding="utf-8")
            payload = {
                "hook_event_name": "PostToolUse",
                "tool_name": "Write",
                "tool_input": {"file_path": str(mission_path)},
            }
            results = self.run_event("PostToolUse", payload, mission_dir, cwd=project_dir)
            self.assertEqual(results[0].returncode, 2, results[0].stderr)
            self.assertIn("missing ## Clarification section", results[0].stderr)

    def test_post_tool_rejects_malformed_clarification_tree(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            mission_dir = Path(tmp) / "missions"
            mission_dir.mkdir()
            mission_path = mission_dir / "brief.md"
            mission_path.write_text(
                brief().replace("  - Answer: It should return `ok`.\n", ""),
                encoding="utf-8",
            )
            payload = {
                "hook_event_name": "PostToolUse",
                "tool_name": "Write",
                "tool_input": {"file_path": str(mission_path)},
            }
            results = self.run_event("PostToolUse", payload, mission_dir)
            self.assertEqual(results[0].returncode, 2, results[0].stderr)
            self.assertIn(
                "Repair the Clarification Tree as recursive Question, Answer, Updated understanding, and Follow-ups nodes.",
                results[0].stderr,
            )
            self.assertIn("must be indented 2 spaces and start with '- Answer:'", results[0].stderr)

    def test_post_tool_rejects_unresolved_clarification_leaf(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            mission_dir = Path(tmp) / "missions"
            mission_dir.mkdir()
            mission_path = mission_dir / "brief.md"
            mission_path.write_text(
                brief().replace("      - Follow-ups: none\n", "      - Follow-ups: pending\n", 1),
                encoding="utf-8",
            )
            payload = {
                "hook_event_name": "PostToolUse",
                "tool_name": "Write",
                "tool_input": {"file_path": str(mission_path)},
            }
            results = self.run_event("PostToolUse", payload, mission_dir)
            self.assertEqual(results[0].returncode, 2, results[0].stderr)
            self.assertIn(
                "Go back to the user and resolve every open clarification branch before revising the mission brief.",
                results[0].stderr,
            )
            self.assertIn("Follow-ups must be nested Question nodes or exactly 'none'", results[0].stderr)

    def test_recursive_clarification_tree_rejects_linear_legacy_shape(self) -> None:
        guard = load_guard_module()
        legacy_tree = textwrap.dedent(
            """\
            - Desired sample behavior: needed to define the observable outcome.
              - Asked: What should the sample command return?
              - Answered: It should return `ok`.
              - Updated understanding: The command should return `ok`.
              - Remaining ambiguity: none
            """
        )
        with self.assertRaisesRegex(guard.ClarificationTreeError, "must start a Question node"):
            guard.parse_clarification_tree(legacy_tree)

    def test_recursive_clarification_tree_rejects_malformed_child_indentation(self) -> None:
        guard = load_guard_module()
        malformed_tree = textwrap.dedent(
            """\
            - Question: What should the command return?
              - Answer: It should return `ok`.
              - Updated understanding: The expected output is `ok`.
              - Follow-ups:
                  - Question: Should it include a newline?
                    - Answer: No.
                    - Updated understanding: The output has no trailing newline.
                    - Follow-ups: none
            """
        )
        with self.assertRaisesRegex(guard.ClarificationTreeError, "unexpected indentation"):
            guard.parse_clarification_tree(malformed_tree)

    def test_recursive_clarification_tree_rejects_empty_follow_up_branch(self) -> None:
        guard = load_guard_module()
        incomplete_tree = textwrap.dedent(
            """\
            - Question: What should the command return?
              - Answer: It should return `ok`.
              - Updated understanding: The expected output is `ok`.
              - Follow-ups:
            """
        )
        with self.assertRaisesRegex(guard.UnresolvedClarificationError, "nested Question node"):
            guard.parse_clarification_tree(incomplete_tree)

    def test_recursive_clarification_tree_rejects_placeholder_content(self) -> None:
        guard = load_guard_module()
        placeholder_tree = textwrap.dedent(
            """\
            - Question: What should the command return?
              - Answer: <verbatim user answer>
              - Updated understanding: The answer defines the expected output.
              - Follow-ups: none
            """
        )
        with self.assertRaisesRegex(guard.UnresolvedClarificationError, "instead of a placeholder"):
            guard.parse_clarification_tree(placeholder_tree)

    def test_post_tool_validates_updated_mission_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            mission_dir = Path(tmp) / "missions"
            mission_dir.mkdir()
            old_bad = mission_dir / "old.md"
            latest_good = mission_dir / "latest.md"
            old_bad.write_text(brief(omit_clarification=True), encoding="utf-8")
            latest_good.write_text(brief("Pending"), encoding="utf-8")
            os.utime(old_bad, (1, 1))
            os.utime(latest_good, (2, 2))
            payload = {"hook_event_name": "PostToolUse", "tool_name": "Write", "tool_input": {"file_path": str(latest_good)}}
            results = self.run_event("PostToolUse", payload, mission_dir)
            self.assertEqual(results[0].returncode, 0, results[0].stderr)

    def test_post_tool_validates_updated_file_even_when_it_is_not_latest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            mission_dir = Path(tmp) / "missions"
            mission_dir.mkdir()
            old_bad = mission_dir / "old.md"
            latest_good = mission_dir / "latest.md"
            old_bad.write_text(brief(omit_clarification=True), encoding="utf-8")
            latest_good.write_text(brief("Pending"), encoding="utf-8")
            os.utime(old_bad, (1, 1))
            os.utime(latest_good, (2, 2))
            payload = {"hook_event_name": "PostToolUse", "tool_name": "Write", "tool_input": {"file_path": str(old_bad)}}
            results = self.run_event("PostToolUse", payload, mission_dir)
            self.assertEqual(results[0].returncode, 2, results[0].stderr)
            self.assertIn("missing ## Clarification section", results[0].stderr)

    def test_post_tool_validates_latest_mission_file_from_patch_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            mission_dir = Path(tmp) / "missions"
            mission_dir.mkdir()
            mission_path = mission_dir / "brief.md"
            mission_path.write_text(brief(omit_clarification=True), encoding="utf-8")
            payload = {
                "hook_event_name": "PostToolUse",
                "tool_name": "apply_patch",
                "tool_input": {
                    "patch": textwrap.dedent(
                        f"""\
                        *** Begin Patch
                        *** Update File: {mission_path}
                        @@
                        *** End Patch
                        """
                    )
                },
            }
            results = self.run_event("PostToolUse", payload, mission_dir)
            self.assertEqual(results[0].returncode, 2, results[0].stderr)
            self.assertIn("missing ## Clarification section", results[0].stderr)

    def test_post_tool_validates_apply_patch_command_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            mission_dir = Path(tmp) / "missions"
            mission_dir.mkdir()
            mission_path = mission_dir / "brief.md"
            mission_path.write_text(brief(omit_clarification=True), encoding="utf-8")
            payload = {
                "hook_event_name": "PostToolUse",
                "tool_name": "apply_patch",
                "tool_input": {
                    "command": textwrap.dedent(
                        f"""\
                        *** Begin Patch
                        *** Add File: {mission_path}
                        +# Mission Brief
                        +bad
                        *** End Patch
                        """
                    )
                },
            }
            results = self.run_event("PostToolUse", payload, mission_dir)
            self.assertEqual(results[0].returncode, 2, results[0].stderr)
            self.assertIn("missing ## Clarification section", results[0].stderr)

if __name__ == "__main__":
    unittest.main()
