#!/usr/bin/env bash
# run: bash agents/deploy.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

SOURCE_CONFIG="${SCRIPT_DIR}/codex/config.toml"
SOURCE_AGENTS="${SCRIPT_DIR}/AGENTS.md"
SOURCE_SKILLS_DIR="${SCRIPT_DIR}/skills"
SOURCE_CLAUDE_SETTINGS="${SCRIPT_DIR}/claude/settings.json"

CODEX_DIR="${HOME}/.codex"
CODEX_SKILLS_DIR="${CODEX_DIR}/skills"
CODEX_BACKUP_ROOT="${CODEX_DIR}/backups"

CLAUDE_DIR="${HOME}/.claude"
CLAUDE_COMMANDS_DIR="${CLAUDE_DIR}/commands"
CLAUDE_BACKUP_ROOT="${CLAUDE_DIR}/backups"

for f in "${SOURCE_CONFIG}" "${SOURCE_AGENTS}" "${SOURCE_CLAUDE_SETTINGS}"; do
  if [[ ! -f "${f}" ]]; then
    echo "Error: missing source file: ${f}" >&2
    exit 1
  fi
done

if [[ ! -d "${SOURCE_SKILLS_DIR}" ]]; then
  echo "Error: missing source directory: ${SOURCE_SKILLS_DIR}" >&2
  exit 1
fi

# --- Codex deployment ---

mkdir -p "${CODEX_DIR}" "${CODEX_SKILLS_DIR}"

STAMP="$(date +%Y%m%d_%H%M%S)"

# --- Codex deployment ---

mkdir -p "${CODEX_DIR}" "${CODEX_SKILLS_DIR}"

CODEX_BACKUP_DIR="${CODEX_BACKUP_ROOT}/${STAMP}"
CODEX_BACKED_UP=0

if [[ -f "${CODEX_DIR}/config.toml" || -f "${CODEX_DIR}/AGENTS.md" ]]; then
  mkdir -p "${CODEX_BACKUP_DIR}"
  [[ -f "${CODEX_DIR}/config.toml" ]] && cp -f "${CODEX_DIR}/config.toml" "${CODEX_BACKUP_DIR}/config.toml" && CODEX_BACKED_UP=1
  [[ -f "${CODEX_DIR}/AGENTS.md" ]]   && cp -f "${CODEX_DIR}/AGENTS.md"   "${CODEX_BACKUP_DIR}/AGENTS.md"   && CODEX_BACKED_UP=1
fi

cp -f "${SOURCE_CONFIG}" "${CODEX_DIR}/config.toml"
cp -f "${SOURCE_AGENTS}" "${CODEX_DIR}/AGENTS.md"

for skill_dir in "${SOURCE_SKILLS_DIR}"/*/; do
  skill_name="$(basename "${skill_dir}")"
  dest="${CODEX_SKILLS_DIR}/${skill_name}"
  mkdir -p "${dest}"
  cp -a "${skill_dir}." "${dest}/"
done

echo "Codex files deployed to ${CODEX_DIR}"
echo "- ${CODEX_DIR}/config.toml"
echo "- ${CODEX_DIR}/AGENTS.md"
echo "- ${CODEX_SKILLS_DIR}"
[[ "${CODEX_BACKED_UP}" -eq 1 ]] && echo "Backup created at ${CODEX_BACKUP_DIR}"

# --- Claude Code deployment ---

mkdir -p "${CLAUDE_DIR}" "${CLAUDE_COMMANDS_DIR}"

CLAUDE_BACKUP_DIR="${CLAUDE_BACKUP_ROOT}/${STAMP}"
CLAUDE_BACKED_UP=0

if [[ -f "${CLAUDE_DIR}/CLAUDE.md" || -f "${CLAUDE_DIR}/settings.json" ]]; then
  mkdir -p "${CLAUDE_BACKUP_DIR}"
  [[ -f "${CLAUDE_DIR}/CLAUDE.md" ]]     && cp -f "${CLAUDE_DIR}/CLAUDE.md"     "${CLAUDE_BACKUP_DIR}/CLAUDE.md"     && CLAUDE_BACKED_UP=1
  [[ -f "${CLAUDE_DIR}/settings.json" ]] && cp -f "${CLAUDE_DIR}/settings.json" "${CLAUDE_BACKUP_DIR}/settings.json" && CLAUDE_BACKED_UP=1
fi

cp -f "${SOURCE_AGENTS}" "${CLAUDE_DIR}/CLAUDE.md"
cp -f "${SOURCE_CLAUDE_SETTINGS}" "${CLAUDE_DIR}/settings.json"

for skill_dir in "${SOURCE_SKILLS_DIR}"/*/; do
  skill_name="$(basename "${skill_dir}")"
  skill_md="${skill_dir}SKILL.md"
  if [[ -f "${skill_md}" ]]; then
    cp -f "${skill_md}" "${CLAUDE_COMMANDS_DIR}/${skill_name}.md"
  fi
done

echo "Claude Code files deployed to ${CLAUDE_DIR}"
echo "- ${CLAUDE_DIR}/CLAUDE.md"
echo "- ${CLAUDE_DIR}/settings.json"
echo "- ${CLAUDE_COMMANDS_DIR}"
[[ "${CLAUDE_BACKED_UP}" -eq 1 ]] && echo "Backup created at ${CLAUDE_BACKUP_DIR}"

# --- Install CLIs ---

ensure_npm() {
  if ! command -v npm &>/dev/null; then
    case "$(uname -s)" in
      Darwin)
        brew install node
        ;;
      Linux)
        if command -v apt-get &>/dev/null; then
          sudo apt-get install -y npm
        elif command -v dnf &>/dev/null; then
          sudo dnf install -y npm
        elif command -v yum &>/dev/null; then
          sudo yum install -y npm
        else
          echo "Error: unsupported package manager — install npm manually" >&2
          exit 1
        fi
        ;;
      *)
        echo "Error: unsupported OS — install npm manually" >&2
        exit 1
        ;;
    esac
  fi
}

if ! command -v codex &>/dev/null; then
  ensure_npm
  npm install -g @openai/codex
  echo "Codex CLI installed"
else
  echo "Codex CLI already installed: $(command -v codex)"
fi

if ! command -v claude &>/dev/null; then
  ensure_npm
  npm install -g @anthropic-ai/claude-code
  echo "Claude Code CLI installed"
else
  echo "Claude Code CLI already installed: $(command -v claude)"
fi
