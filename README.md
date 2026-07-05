# codewizard

Configuration and deployment files for AI coding agents. Supports both **OpenAI Codex** and **Claude Code**.

## Structure

```
agents/
├── AGENTS.md              # shared root policy (writing, task routing)
├── deploy.sh              # legacy local deploy to both ~/.codex and ~/.claude
├── codex/
│   └── config.toml        # Codex-specific: model, approval policy, sandbox mode
├── claude/
│   └── settings.json      # Claude Code-specific: model, permissions
└── tests/                 # skill test harnesses

.agents/
└── plugins/
    └── marketplace.json   # GitHub-hosted Codex marketplace catalog

plugins/
└── codewizard/
    ├── .codex-plugin/
    │   └── plugin.json    # Codex plugin manifest
    └── skills/            # runtime skills shipped by the plugin
        ├── code-mission/
        ├── code-review-expert/
        ├── commit-and-pr/
        ├── isolated-worktree/
        ├── research/
        └── system-design/
```

## Install

### Codex

Install from the GitHub-hosted Codex marketplace:

```bash
codex plugin marketplace add GUG11/codewizard --ref master
codex plugin add codewizard@codewizard
```

Start a new Codex thread after installing so the bundled skills are available.

### Claude Code

Load the plugin from a cloned checkout:

```bash
claude --plugin-dir /absolute/path/to/codewizard/plugins/codewizard
```

Load the plugin from a GitHub release zip:

```bash
claude --plugin-url https://github.com/GUG11/codewizard/releases/download/<version>/codewizard-plugin.zip
```

The release zip must contain the contents of `plugins/codewizard` at the zip root. Build it with:

```bash
mkdir -p dist
(cd plugins/codewizard && zip -r ../../dist/codewizard-plugin.zip .)
```

### Local Config Deploy

```bash
bash agents/deploy.sh
```

`agents/deploy.sh` does not install skills or plugins. It only copies shared guidance and local config files.

**Codex** (`~/.codex`):
- Copies `codex/config.toml` and `AGENTS.md`
- Backs up existing Codex files before overwriting

**Claude Code** (`~/.claude`):
- Copies `AGENTS.md` as `CLAUDE.md`
- Copies `claude/settings.json`
- Backs up existing Claude Code files before overwriting

## Skills

| Skill | Description |
|---|---|
| `code-mission` | Create a mission brief, implement, verify, and review |
| `code-review-expert` | Senior engineer review: SOLID, security, performance |
| `commit-and-pr` | Draft commit messages and PR descriptions from diffs |
| `isolated-worktree` | Manage concurrent local work through isolated worktrees |
| `research` | Search, evaluate, decompose, and synthesize before acting |
| `system-design` | System design guidance |

## Other

- `conf/vscode/user_settings.json`: editor settings
