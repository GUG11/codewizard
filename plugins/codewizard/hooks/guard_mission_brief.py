#!/usr/bin/env python3
"""Validate modified code-mission brief files after tool execution."""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any, NamedTuple


MISSION_DIR = Path(os.environ.get("CODE_MISSION_DIR", "/tmp/docs/missions"))
ALLOWED_TOP_SECTIONS = [
    "Initial User Request",
    "Formal Requirements",
    "Approval Status",
    "Mission Status",
    "Clarification",
    "User Feedback",
]
ALLOWED_CLARIFICATION_SUBSECTIONS = ["Clarification Tree", "Clarified Intent"]
CLARIFICATION_MARKERS = ("- ", "  - Asked:", "  - Answered:", "  - Updated understanding:", "  - Remaining ambiguity:")
ACTION_BY_FAILURE_CODE = {
    "approval_status": "Set a valid Approval Status based on the current situation. Zero tolerance for forging the user's approval",
    "clarification_sections": "Rewrite the Clarification section to contain only ### Clarification Tree and ### Clarified Intent.",
    "clarification_tree": "Repair the Clarification Tree with the required Asked, Answered, Updated understanding, and Remaining ambiguity entries.",
    "formal_requirements": "Repair Formal Requirements as a table with Requirement and Result columns.",
    "missing_clarification": "Start the code-mission clarification process with the user before creating or revising the mission brief.",
    "remaining_ambiguity": "Go back to the user and resolve the remaining mission-critical ambiguity before revising the mission brief.",
    "title": "Change the title to '# Mission Brief: <short title>'.",
    "top_sections": "Rewrite the mission brief to match the template exactly; remove sections not defined by the template.",
    "unreadable": "Rewrite the latest mission brief file so it is readable at the expected path.",
}


class ParsedBrief(NamedTuple):
    text: str
    title_ok: bool
    sections: dict[str, str]
    section_order: list[str]
    clarification_sections: dict[str, str]
    clarification_order: list[str]


class ParsedBlocks(NamedTuple):
    body: dict[str, str]
    order: list[str]


class Failure(NamedTuple):
    code: str
    message: str


def main() -> int:
    payload = read_payload()
    latest = latest_mission_path()
    if latest is None or latest not in updated_paths(payload):
        return 0

    failures = validate_mission_path(latest)

    if failures:
        print_blocked_action(failures)
        return 2
    return 0


def print_blocked_action(failures: list[Failure]) -> None:
    print("code-mission guard blocked this action.", file=sys.stderr)
    print("Next action:", file=sys.stderr)
    for action in recovery_actions(failures):
        print(f"- {action}", file=sys.stderr)
    print("Refer to the code-mission skill instructions for the required mission brief format and approval rules.", file=sys.stderr)
    print("Failures:", file=sys.stderr)
    for failure in failures:
        print(f"- {failure.message}", file=sys.stderr)


def recovery_actions(failures: list[Failure]) -> list[str]:
    codes = {failure.code for failure in failures}
    actions: list[str] = []
    missing_actions = sorted(codes - ACTION_BY_FAILURE_CODE.keys())
    if missing_actions:
        raise AssertionError(f"missing recovery action for failure code(s): {', '.join(missing_actions)}")
    for code in ACTION_BY_FAILURE_CODE:
        if code in codes and ACTION_BY_FAILURE_CODE[code] not in actions:
            actions.append(ACTION_BY_FAILURE_CODE[code])
    return actions


def validate_mission_path(path: Path) -> list[Failure]:
    if not path.is_file():
        return [Failure("unreadable", f"{path}: mission brief was modified but is not readable after the tool ran")]
    text = path.read_text(encoding="utf-8")
    return [
        Failure(failure.code, f"{path}: {failure.message}")
        for failure in validate_mission_brief(parse_mission_brief(text))
    ]


def latest_mission_path() -> Path | None:
    try:
        files = [path for path in MISSION_DIR.iterdir() if path.is_file() and path.suffix == ".md"]
    except OSError:
        return None
    if not files:
        return None
    return max(files, key=lambda path: (path.stat().st_mtime_ns, path.name)).resolve()


def parse_mission_brief(text: str) -> ParsedBrief:
    sections = parse_heading_blocks(text, 2)
    clarification = sections.body.get("Clarification", "")
    clarification_sections = parse_heading_blocks(clarification, 3)
    return ParsedBrief(
        text=text,
        title_ok=bool(re.search(r"(?m)^# Mission Brief: .+\S$", text)),
        sections=sections.body,
        section_order=sections.order,
        clarification_sections=clarification_sections.body,
        clarification_order=clarification_sections.order,
    )


def parse_heading_blocks(text: str, level: int) -> ParsedBlocks:
    marker = "#" * level
    pattern = re.compile(rf"(?m)^{re.escape(marker)} (.+)$")
    matches = list(pattern.finditer(text))
    body: dict[str, str] = {}
    order: list[str] = []
    for index, match in enumerate(matches):
        name = match.group(1)
        start = match.end() + 1
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        order.append(name)
        body[name] = text[start:end]
    return ParsedBlocks(body=body, order=order)


def validate_mission_brief(brief: ParsedBrief) -> list[Failure]:
    failures: list[Failure] = []

    if not brief.title_ok:
        failures.append(Failure("title", "mission brief must start with '# Mission Brief: <short title>'"))

    if brief.section_order != ALLOWED_TOP_SECTIONS:
        failures.append(
            Failure(
                "top_sections",
                "mission brief sections must exactly be: "
                + ", ".join(f"## {section}" for section in ALLOWED_TOP_SECTIONS),
            )
        )

    if "Clarification" not in brief.sections:
        failures.append(Failure("missing_clarification", "missing ## Clarification section"))
    else:
        if brief.clarification_order != ALLOWED_CLARIFICATION_SUBSECTIONS:
            failures.append(
                Failure(
                    "clarification_sections",
                    "Clarification subsections must exactly be: "
                    + ", ".join(f"### {section}" for section in ALLOWED_CLARIFICATION_SUBSECTIONS),
                )
            )
        failures.extend(validate_clarification_tree(brief))

    approval_status = brief.sections.get("Approval Status", "").strip()
    if approval_status not in {"Pending", "Approved", "Rejected"}:
        failures.append(Failure("approval_status", "Approval Status must be exactly Pending, Approved, or Rejected"))

    formal_requirements = brief.sections.get("Formal Requirements", "")
    if "| Requirement |" not in formal_requirements or "| Result |" not in formal_requirements:
        failures.append(Failure("formal_requirements", "Formal Requirements must be a table with Requirement and Result columns"))

    return failures


def validate_clarification_tree(brief: ParsedBrief) -> list[Failure]:
    failures: list[Failure] = []
    tree = brief.clarification_sections.get("Clarification Tree", "")
    if not tree:
        return [Failure("clarification_tree", "missing ### Clarification Tree subsection")]

    for marker in CLARIFICATION_MARKERS:
        if marker not in tree:
            failures.append(Failure("clarification_tree", f"Clarification Tree must include '{marker.strip()}'"))
    if not re.search(r"(?mi)^\s+- Remaining ambiguity:\s*none\s*$", tree):
        failures.append(Failure("remaining_ambiguity", "mission brief cannot be created while Remaining ambiguity is not exactly 'none'"))
    return failures


def read_payload() -> dict[str, Any]:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"code-mission guard blocked this action:\n- hook input was not valid JSON: {exc}", file=sys.stderr)
        sys.exit(2)
    if not isinstance(parsed, dict):
        print("code-mission guard blocked this action:\n- hook input must be a JSON object", file=sys.stderr)
        sys.exit(2)
    return parsed


def updated_paths(payload: dict[str, Any]) -> set[Path]:
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return set()

    paths: set[Path] = set()
    for key in ("file_path", "path"):
        value = tool_input.get(key)
        if isinstance(value, str):
            paths.add(resolve_path(value))

    patch = tool_input.get("patch")
    if not isinstance(patch, str) and payload.get("tool_name") == "apply_patch":
        patch = tool_input.get("command")
    if isinstance(patch, str):
        paths.update(extract_patch_paths(patch))

    return paths


def extract_patch_paths(text: str) -> set[Path]:
    paths: set[Path] = set()
    for line in text.splitlines():
        match = re.match(r"^\*\*\* (?:Add|Update|Delete) File: (.+)$", line) or re.match(r"^\*\*\* Move to: (.+)$", line)
        if match:
            paths.add(resolve_path(match.group(1).strip()))
    return paths


def resolve_path(path: str) -> Path:
    expanded = Path(os.path.expanduser(path))
    if not expanded.is_absolute():
        expanded = Path.cwd() / expanded
    return expanded.resolve()


if __name__ == "__main__":
    sys.exit(main())
