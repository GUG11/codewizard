import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HOOK = ROOT / "plugins/codewizard/hooks/guard_mission_identity.py"


def run_hook(status, target, tool="Write", thread_id="thread"):
    with tempfile.TemporaryDirectory() as tmp:
        mission_dir = Path(tmp) / "missions"
        mission_dir.mkdir()
        if status:
            body = f"# Mission\n\n## Approval Status\n{status}\n\n## Mission Status\nPending.\n"
            (mission_dir / "thread.md").write_text(body, encoding="utf-8")
        target_path = mission_dir / target
        if tool == "apply_patch":
            tool_input = {"patch": f"*** Begin Patch\n*** Add File: {target_path}\n*** End Patch\n"}
        else:
            tool_input = {"file_path": str(target_path)}
        payload = {"hook_event_name": "PreToolUse", "tool_name": tool, "tool_input": tool_input}
        env = os.environ.copy()
        env.update({"CODE_MISSION_DIR": str(mission_dir), "CODEX_THREAD_ID": thread_id, "PYTHONDONTWRITEBYTECODE": "1"})
        return subprocess.run(
            ["python3", str(HOOK)], input=json.dumps(payload), text=True,
            capture_output=True, env=env, check=False,
        )


class MissionIdentityHookTest(unittest.TestCase):
    def test_approval_gate(self):
        cases = (
            (None, "thread.md", "Write", "thread", 0),
            ("Pending", "replacement.md", "Write", "thread", 0),
            ("Rejected", "replacement.md", "Write", "thread", 0),
            ("Approved", "thread.md", "Edit", "thread", 0),
            ("Approved", "replacement.md", "Write", "thread", 2),
            ("Approved", "thread-b.md", "Write", "thread-b", 0),
            ("Approved", "replacement.md", "apply_patch", "thread", 2),
        )
        for status, target, tool, thread_id, expected in cases:
            with self.subTest(status=status, target=target, tool=tool, thread_id=thread_id):
                result = run_hook(status, target, tool, thread_id)
                self.assertEqual(result.returncode, expected, result.stderr)
                if expected == 2:
                    self.assertIn("correction to the existing implementation", result.stderr)
