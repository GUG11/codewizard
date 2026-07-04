# codewizard

Configuration and deployment files for AI coding agents. Supports both **OpenAI Codex** and **Claude Code**.

## Structure

```
agents/
├── AGENTS.md              # shared root policy (writing, task routing)
├── deploy.sh              # deploys to both ~/.codex and ~/.claude
├── codex/
│   └── config.toml        # Codex-specific: model, approval policy, sandbox mode
├── claude/
│   └── settings.json      # Claude Code-specific: model, permissions
├── skills/                # platform-agnostic skills
│   ├── code-mission/
│   │   └── references/languages/
│   │                       # language-specific execution guides
│   ├── code-review-expert-main/
│   ├── commit-and-pr-summary/
│   ├── research/
│   └── system-design/
└── tests/                 # skill test harnesses
```

## Deploy

```bash
bash agents/deploy.sh
```

### What it does

**Codex** (`~/.codex`):
- Copies `codex/config.toml` and `AGENTS.md`
- Copies all skills into `~/.codex/skills/`
- Deploys language guides as code-mission skill references
- Backs up existing Codex files before overwriting

**Claude Code** (`~/.claude`):
- Copies `AGENTS.md` as `CLAUDE.md`
- Copies `claude/settings.json`
- Copies all skills into `~/.claude/skills/`
- Deploys language guides as code-mission skill references
- Removes old generated skill folders from `~/.claude/commands/`
- Backs up existing Claude Code files before overwriting

## Skills

| Skill | Description |
|---|---|
| `code-mission` | Create a mission brief, implement, verify, and review |
| `code-review-expert-main` | Senior engineer review: SOLID, security, performance |
| `commit-and-pr-summary` | Draft commit messages and PR descriptions from diffs |
| `research` | Search, evaluate, decompose, and synthesize before acting |
| `system-design` | System design guidance |

## Other

- `conf/vscode/user_settings.json`: editor settings
