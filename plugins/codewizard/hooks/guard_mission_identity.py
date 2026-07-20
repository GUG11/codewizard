#!/usr/bin/env python3
import json
import os
import re
import sys
from pathlib import Path

MISSION_DIR = Path(os.getenv("CODE_MISSION_DIR", "/tmp/docs/missions")).expanduser().resolve()
BLOCK_PROMPT = (
    "There is already an approved mission in this thread. Now you are creating a new one. "
    "Are you conflating the user's correction to the existing implementation with a new intent?"
)

def main():
    payload = json.load(sys.stdin)
    tool_input = payload["tool_input"]
    thread_id = os.getenv("CODEX_THREAD_ID")
    if not thread_id:
        return 0
    canonical = MISSION_DIR / f"{thread_id}.md"
    try:
        is_approved = "\n## Approval Status\nApproved\n" in canonical.read_text(encoding="utf-8")
    except OSError:
        return 0
    if not is_approved:
        return 0

    values = [tool_input.get("file_path"), tool_input.get("path")]
    patch = tool_input.get("patch") or tool_input.get("command") or ""
    values += re.findall(r"^\*\*\* (?:(?:Add|Update|Delete) File|Move to): (.+)$", patch, re.M)
    for value in filter(None, values):
        path = Path(value).expanduser()
        path = (path if path.is_absolute() else Path.cwd() / path).resolve()
        if path.parent == MISSION_DIR and path.suffix == ".md" and path != canonical:
            print(BLOCK_PROMPT, file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
