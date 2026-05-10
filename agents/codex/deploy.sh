#!/usr/bin/env bash
# run: bash agents/codex/deploy.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENTS_DIR="$(cd "${SCRIPT_DIR}/../" && pwd)"

SOURCE_CONFIG="${SCRIPT_DIR}/config.toml"
SOURCE_AGENTS="${AGENTS_DIR}/AGENTS.md"
SOURCE_SKILLS_DIR="${AGENTS_DIR}/skills"
SOURCE_CODEX_SKILLS_DIR="${SCRIPT_DIR}/skills"

CODEX_DIR="${HOME}/.codex"
CODEX_SKILLS_DIR="${CODEX_DIR}/skills"
BACKUP_ROOT="${CODEX_DIR}/backups"

CLAUDE_DIR="${HOME}/.claude"
CLAUDE_COMMANDS_DIR="${CLAUDE_DIR}/commands"

for f in "${SOURCE_CONFIG}" "${SOURCE_AGENTS}"; do
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
BACKUP_DIR="${BACKUP_ROOT}/${STAMP}"
BACKED_UP=0

if [[ -f "${CODEX_DIR}/config.toml" || -f "${CODEX_DIR}/AGENTS.md" ]]; then
  mkdir -p "${BACKUP_DIR}"

  if [[ -f "${CODEX_DIR}/config.toml" ]]; then
    cp -f "${CODEX_DIR}/config.toml" "${BACKUP_DIR}/config.toml"
    BACKED_UP=1
  fi

  if [[ -f "${CODEX_DIR}/AGENTS.md" ]]; then
    cp -f "${CODEX_DIR}/AGENTS.md" "${BACKUP_DIR}/AGENTS.md"
    BACKED_UP=1
  fi
fi

cp -f "${SOURCE_CONFIG}" "${CODEX_DIR}/config.toml"
cp -f "${SOURCE_AGENTS}" "${CODEX_DIR}/AGENTS.md"

# Deploy shared skill content + Codex-specific agent.yaml into ~/.codex/skills/
for skill_dir in "${SOURCE_SKILLS_DIR}"/*/; do
  skill_name="$(basename "${skill_dir}")"
  dest="${CODEX_SKILLS_DIR}/${skill_name}"
  mkdir -p "${dest}"
  cp -a "${skill_dir}." "${dest}/"
  codex_agents_dir="${SOURCE_CODEX_SKILLS_DIR}/${skill_name}/agents"
  if [[ -d "${codex_agents_dir}" ]]; then
    mkdir -p "${dest}/agents"
    cp -a "${codex_agents_dir}/." "${dest}/agents/"
  fi
done

echo "Codex files deployed to ${CODEX_DIR}"
echo "- ${CODEX_DIR}/config.toml"
echo "- ${CODEX_DIR}/AGENTS.md"
echo "- ${CODEX_SKILLS_DIR}"

if [[ "${BACKED_UP}" -eq 1 ]]; then
  echo "Backup created at ${BACKUP_DIR}"
fi

# --- Claude Code deployment ---

mkdir -p "${CLAUDE_DIR}" "${CLAUDE_COMMANDS_DIR}"

cp -f "${SOURCE_AGENTS}" "${CLAUDE_DIR}/CLAUDE.md"
echo "Claude Code files deployed to ${CLAUDE_DIR}"
echo "- ${CLAUDE_DIR}/CLAUDE.md"

for skill_dir in "${SOURCE_SKILLS_DIR}"/*/; do
  skill_name="$(basename "${skill_dir}")"
  skill_md="${skill_dir}SKILL.md"
  if [[ -f "${skill_md}" ]]; then
    cp -f "${skill_md}" "${CLAUDE_COMMANDS_DIR}/${skill_name}.md"
    echo "- ${CLAUDE_COMMANDS_DIR}/${skill_name}.md"
  fi
done

sudo apt install npm -y
sudo npm install -g @openai/codex
