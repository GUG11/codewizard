#!/usr/bin/env python3

import ipaddress
import json
import re
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

WORD_RE = re.compile(r"\b\w+(?:['’]\w+)*\b")
RECOMMENDATION_RE = re.compile(r"\brecommendations?\b", re.I)
AMBIGUITY_RE = re.compile(r"\b(?:caveat|unknown|unclear)s?\b", re.I)
IF_RE = re.compile(r"\bifs?\b", re.I)
URL_RE = re.compile(r"https?://[^\s<>\"']*", re.I)


def non_code_text(text: str) -> str:
    return re.sub(r"`[^`\n]*`", " ", re.sub(r"(?s)(```|~~~).*?\1", " ", text))


def extract_urls(text: str) -> list[str]:
    urls = []
    for match in URL_RE.finditer(non_code_text(text)):
        url = match.group().rstrip(".,;:!?]}")
        while url.endswith(")") and url.count(")") > url.count("("):
            url = url[:-1]
        if url and url not in urls:
            urls.append(url)
    return urls


def check_url(url: str) -> str:
    try:
        parsed = urllib.parse.urlsplit(url)
        host = parsed.hostname
        if parsed.scheme.lower() not in {"http", "https"} or not host:
            return "malformed URL"
    except ValueError:
        return "malformed URL"
    try:
        addresses = socket.getaddrinfo(host, parsed.port or (443 if parsed.scheme.lower() == "https" else 80), type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        return "domain does not exist" if exc.errno == socket.EAI_NONAME else ""
    if not addresses or any(not ipaddress.ip_address(item[4][0]).is_global for item in addresses):
        return ""
    request = urllib.request.Request(url, headers={"User-Agent": "CodeWizard-Link-Validator", "Range": "bytes=0-0"})
    try:
        urllib.request.urlopen(request, timeout=5).close()
    except urllib.error.HTTPError as exc:
        return f"HTTP {exc.code}" if exc.code in {404, 410} else ""
    except urllib.error.URLError as exc:
        reason = exc.reason
        return "domain does not exist" if isinstance(reason, socket.gaierror) and reason.errno == socket.EAI_NONAME else ""
    except (OSError, TimeoutError, ValueError):
        return ""
    return ""


def validate_response(text: str) -> list[str]:
    failures = []
    word_count = len(WORD_RE.findall(text))
    if word_count > 500:
        failures.append(
            f"The response contains {word_count} words. To simplify it, remove Defensive and Conservative Wording and worthless words."
        )
    prose = URL_RE.sub(" ", non_code_text(text))
    if RECOMMENDATION_RE.search(prose):
        failures.append(
            "Your answer includes a recommendation. Are you asking the user to take action? Do not teach the user what to do; do it yourself."
        )
    ambiguities = tuple(dict.fromkeys(match.group().lower() for match in AMBIGUITY_RE.finditer(prose)))
    if ambiguities:
        failures.append(
            f"Your answer includes {', '.join(ambiguities)}. Have you exhausted all available information? Use every available tool and source to find the answer instead of leaving ambiguity."
        )
    if IF_RE.search(prose):
        failures.append(
            "Your answer includes an if-condition, which is intolerable. Verify the facts and answer directly. No if-based speculation."
        )
    links = extract_urls(text)
    if links:
        with ThreadPoolExecutor(max_workers=min(8, len(links))) as executor:
            broken = [(url, reason) for url, reason in zip(links, executor.map(check_url, links)) if reason]
        if broken:
            details = "; ".join(f"{url} ({reason})" for url, reason in broken)
            failures.append(f"Broken links: {details}. Correct or remove every broken link.")
    return failures


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        response = payload.get("last_assistant_message") if isinstance(payload, dict) else None
    except (OSError, ValueError):
        return 0
    if not isinstance(response, str) or not response.strip():
        return 0
    failures = validate_response(response)
    if not failures:
        return 0
    reason = "\n".join(f"- {failure}" for failure in failures)
    if payload.get("stop_hook_active") is True:
        message = "Response quality guard allowed the turn after one correction attempt to prevent a Stop-hook loop. Remaining violations:\n"
        print(json.dumps({"systemMessage": message + reason}))
    else:
        print(json.dumps({"decision": "block", "reason": reason}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
