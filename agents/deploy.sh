#!/usr/bin/env bash
# run: bash agents/deploy.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

SOURCE_CONFIG="${SCRIPT_DIR}/codex/config.toml"
SOURCE_AGENTS="${SCRIPT_DIR}/AGENTS.md"
SOURCE_CLAUDE_SETTINGS="${SCRIPT_DIR}/claude/settings.json"

CODEX_DIR="${HOME}/.codex"
CODEX_BACKUP_ROOT="${CODEX_DIR}/backups"

CLAUDE_DIR="${HOME}/.claude"
CLAUDE_BACKUP_ROOT="${CLAUDE_DIR}/backups"

for f in "${SOURCE_CONFIG}" "${SOURCE_AGENTS}" "${SOURCE_CLAUDE_SETTINGS}"; do
  if [[ ! -f "${f}" ]]; then
    echo "Error: missing source file: ${f}" >&2
    exit 1
  fi
done

STAMP="$(date +%Y%m%d_%H%M%S)"

# --- Codex deployment ---

mkdir -p "${CODEX_DIR}"

CODEX_BACKUP_DIR="${CODEX_BACKUP_ROOT}/${STAMP}"
CODEX_BACKED_UP=0

if [[ -f "${CODEX_DIR}/config.toml" || -f "${CODEX_DIR}/AGENTS.md" ]]; then
  mkdir -p "${CODEX_BACKUP_DIR}"
  [[ -f "${CODEX_DIR}/config.toml" ]] && cp -f "${CODEX_DIR}/config.toml" "${CODEX_BACKUP_DIR}/config.toml" && CODEX_BACKED_UP=1
  [[ -f "${CODEX_DIR}/AGENTS.md" ]]   && cp -f "${CODEX_DIR}/AGENTS.md"   "${CODEX_BACKUP_DIR}/AGENTS.md"   && CODEX_BACKED_UP=1
fi

cp -f "${SOURCE_CONFIG}" "${CODEX_DIR}/config.toml"
cp -f "${SOURCE_AGENTS}" "${CODEX_DIR}/AGENTS.md"

echo "Codex files deployed to ${CODEX_DIR}"
echo "- ${CODEX_DIR}/config.toml"
echo "- ${CODEX_DIR}/AGENTS.md"
[[ "${CODEX_BACKED_UP}" -eq 1 ]] && echo "Backup created at ${CODEX_BACKUP_DIR}"

# --- Claude Code deployment ---

mkdir -p "${CLAUDE_DIR}"

CLAUDE_BACKUP_DIR="${CLAUDE_BACKUP_ROOT}/${STAMP}"
CLAUDE_BACKED_UP=0

if [[ -f "${CLAUDE_DIR}/CLAUDE.md" || -f "${CLAUDE_DIR}/settings.json" ]]; then
  mkdir -p "${CLAUDE_BACKUP_DIR}"
  [[ -f "${CLAUDE_DIR}/CLAUDE.md" ]]     && cp -f "${CLAUDE_DIR}/CLAUDE.md"     "${CLAUDE_BACKUP_DIR}/CLAUDE.md"     && CLAUDE_BACKED_UP=1
  [[ -f "${CLAUDE_DIR}/settings.json" ]] && cp -f "${CLAUDE_DIR}/settings.json" "${CLAUDE_BACKUP_DIR}/settings.json" && CLAUDE_BACKED_UP=1
fi

cp -f "${SOURCE_AGENTS}" "${CLAUDE_DIR}/CLAUDE.md"
cp -f "${SOURCE_CLAUDE_SETTINGS}" "${CLAUDE_DIR}/settings.json"

echo "Claude Code files deployed to ${CLAUDE_DIR}"
echo "- ${CLAUDE_DIR}/CLAUDE.md"
echo "- ${CLAUDE_DIR}/settings.json"
[[ "${CLAUDE_BACKED_UP}" -eq 1 ]] && echo "Backup created at ${CLAUDE_BACKUP_DIR}"
