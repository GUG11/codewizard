# codewizard

Configuration and deployment files for a Codex agent setup.

## Contents

- `agents/codex/config.toml`: default Codex agent configuration
- `agents/codex/AGENTS.md`: repository-level agent instructions
- `agents/codex/deploy.sh`: copies the Codex config, instructions, and skills into `~/.codex`
- `agents/codex/skills/`: local Codex skills shipped with this repo
- `conf/vscode/user_settings.json`: editor settings

## Deploy

Run:

```bash
bash agents/codex/deploy.sh
```

The script:

- copies `config.toml` and `AGENTS.md` into `~/.codex`
- copies bundled skills into `~/.codex/skills`
- creates backups of existing Codex files when present
- installs `@openai/codex` with `npm`
