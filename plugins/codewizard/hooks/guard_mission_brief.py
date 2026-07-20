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
ACTION_BY_FAILURE_CODE = {
    "approval_status": "Set a valid Approval Status based on the current situation. Zero tolerance for forging the user's approval",
    "clarification_sections": "Rewrite the Clarification section to contain only ### Clarification Tree and ### Clarified Intent.",
    "clarification_tree": "Repair the Clarification Tree as recursive Question, Answer, Updated understanding, and Follow-ups nodes.",
    "formal_requirements": "Repair Formal Requirements as a table with Requirement and Result columns.",
    "missing_clarification": "Start the code-mission clarification process with the user before creating or revising the mission brief.",
    "title": "Change the title to '# Mission Brief: <short title>'.",
    "top_sections": "Rewrite the mission brief to match the template exactly; remove sections not defined by the template.",
    "unresolved_clarification": "Go back to the user and resolve every open clarification branch before revising the mission brief.",
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


class TreeLine(NamedTuple):
    number: int
    indent: int
    content: str


class ClarificationTreeError(ValueError):
    pass


class UnresolvedClarificationError(ClarificationTreeError):
    pass


def main() -> int:
    payload = read_payload()
    paths = updated_mission_paths(payload)
    if not paths:
        return 0

    failures = [failure for path in sorted(paths) for failure in validate_mission_path(path)]

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


def updated_mission_paths(payload: dict[str, Any]) -> set[Path]:
    mission_dir = MISSION_DIR.resolve()
    return {
        path
        for path in updated_paths(payload)
        if path.parent == mission_dir and path.suffix == ".md"
    }


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
    tree = brief.clarification_sections.get("Clarification Tree", "")
    if not tree:
        return [Failure("clarification_tree", "missing ### Clarification Tree subsection")]

    try:
        parse_clarification_tree(tree)
    except UnresolvedClarificationError as exc:
        return [Failure("unresolved_clarification", str(exc))]
    except ClarificationTreeError as exc:
        return [Failure("clarification_tree", str(exc))]
    return []


def parse_clarification_tree(tree: str) -> None:
    lines = clarification_tree_lines(tree)
    if not lines:
        raise ClarificationTreeError("Clarification Tree must contain at least one Question node")
    next_index = parse_question_nodes(lines, 0, 0)
    if next_index != len(lines):
        line = lines[next_index]
        raise ClarificationTreeError(f"Clarification Tree line {line.number} has unexpected indentation or content: {line.content}")


def clarification_tree_lines(tree: str) -> list[TreeLine]:
    lines: list[TreeLine] = []
    for number, raw_line in enumerate(tree.splitlines(), start=1):
        if not raw_line.strip():
            continue
        content = raw_line.lstrip(" ")
        indent = len(raw_line) - len(content)
        if content.startswith("\t"):
            raise ClarificationTreeError(f"Clarification Tree line {number} must use spaces for indentation")
        lines.append(TreeLine(number=number, indent=indent, content=content.rstrip()))
    return lines


def parse_question_nodes(lines: list[TreeLine], index: int, indent: int) -> int:
    node_count = 0
    while index < len(lines):
        line = lines[index]
        if line.indent < indent:
            break
        if line.indent > indent:
            raise ClarificationTreeError(f"Clarification Tree line {line.number} has unexpected indentation")
        if not line.content.startswith("- Question:"):
            raise ClarificationTreeError(f"Clarification Tree line {line.number} must start a Question node")
        index = parse_question_node(lines, index, indent)
        node_count += 1
    if node_count == 0:
        line_number = lines[index].number if index < len(lines) else lines[-1].number
        raise UnresolvedClarificationError(
            f"Clarification Tree line {line_number} must contain a nested Question node or declare 'Follow-ups: none'"
        )
    return index


def parse_question_node(lines: list[TreeLine], index: int, indent: int) -> int:
    question, index = parse_tree_field(lines, index, indent, "Question")
    answer, index = parse_tree_field(lines, index, indent + 2, "Answer")
    understanding, index = parse_tree_field(lines, index, indent + 2, "Updated understanding")
    follow_ups, index = parse_tree_field(lines, index, indent + 2, "Follow-ups", allow_empty=True)

    for field_name, value in (
        ("Question", question),
        ("Answer", answer),
        ("Updated understanding", understanding),
    ):
        if is_placeholder(value):
            raise UnresolvedClarificationError(
                f"Clarification Tree {field_name} must contain resolved content instead of a placeholder"
            )

    if follow_ups.casefold() == "none":
        return index
    if follow_ups:
        raise UnresolvedClarificationError(
            "Clarification Tree Follow-ups must be nested Question nodes or exactly 'none'"
        )
    return parse_question_nodes(lines, index, indent + 4)


def parse_tree_field(
    lines: list[TreeLine],
    index: int,
    indent: int,
    field_name: str,
    allow_empty: bool = False,
) -> tuple[str, int]:
    if index >= len(lines):
        raise ClarificationTreeError(f"Clarification Tree ended before '- {field_name}:'")
    line = lines[index]
    prefix = f"- {field_name}:"
    if line.indent != indent or not line.content.startswith(prefix):
        raise ClarificationTreeError(
            f"Clarification Tree line {line.number} must be indented {indent} spaces and start with '{prefix}'"
        )
    value = line.content[len(prefix) :].strip()
    if not value and not allow_empty:
        raise UnresolvedClarificationError(f"Clarification Tree line {line.number} has an empty {field_name}")
    return value, index + 1


def is_placeholder(value: str) -> bool:
    stripped = value.strip()
    return bool(re.fullmatch(r"<[^>]+>", stripped)) or stripped.casefold() in {"pending", "tbd", "unresolved"}


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
