#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_CONFIG="${SCRIPT_DIR}/config.toml"
SOURCE_AGENTS="${SCRIPT_DIR}/AGENTS.md"
SOURCE_SKILLS_DIR="${SCRIPT_DIR}/skills"
TARGET_DIR="${HOME}/.codex"
TARGET_SKILLS_DIR="${TARGET_DIR}/skills"
BACKUP_ROOT="${TARGET_DIR}/backups"

if [[ ! -f "${SOURCE_CONFIG}" ]]; then
  echo "Error: missing source file: ${SOURCE_CONFIG}" >&2
  exit 1
fi

if [[ ! -f "${SOURCE_AGENTS}" ]]; then
  echo "Error: missing source file: ${SOURCE_AGENTS}" >&2
  exit 1
fi

mkdir -p "${TARGET_DIR}"
mkdir -p "${TARGET_SKILLS_DIR}"

STAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_DIR="${BACKUP_ROOT}/${STAMP}"
BACKED_UP=0

if [[ -f "${TARGET_DIR}/config.toml" || -f "${TARGET_DIR}/AGENTS.md" ]]; then
  mkdir -p "${BACKUP_DIR}"

  if [[ -f "${TARGET_DIR}/config.toml" ]]; then
    cp -f "${TARGET_DIR}/config.toml" "${BACKUP_DIR}/config.toml"
    BACKED_UP=1
  fi

  if [[ -f "${TARGET_DIR}/AGENTS.md" ]]; then
    cp -f "${TARGET_DIR}/AGENTS.md" "${BACKUP_DIR}/AGENTS.md"
    BACKED_UP=1
  fi
fi

cp -f "${SOURCE_CONFIG}" "${TARGET_DIR}/config.toml"
cp -f "${SOURCE_AGENTS}" "${TARGET_DIR}/AGENTS.md"

if [[ -d "${SOURCE_SKILLS_DIR}" ]]; then
  for skill_dir in "${SOURCE_SKILLS_DIR}"/*; do
    if [[ -d "${skill_dir}" && -f "${skill_dir}/SKILL.md" ]]; then
      skill_name="$(basename "${skill_dir}")"
      mkdir -p "${TARGET_SKILLS_DIR}/${skill_name}"
      cp -f "${skill_dir}/SKILL.md" "${TARGET_SKILLS_DIR}/${skill_name}/SKILL.md"
    fi
  done
fi

mkdir -p "${TARGET_SKILLS_DIR}/skill-creator"
curl -fsSL \
  "https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md" \
  -o "${TARGET_SKILLS_DIR}/skill-creator/SKILL.md"

echo "Codex files deployed to ${TARGET_DIR}"
echo "- ${TARGET_DIR}/config.toml"
echo "- ${TARGET_DIR}/AGENTS.md"
echo "- ${TARGET_SKILLS_DIR}/bug-fix-loop/SKILL.md"
echo "- ${TARGET_SKILLS_DIR}/test-strategy/SKILL.md"
echo "- ${TARGET_SKILLS_DIR}/perf-sanity/SKILL.md"
echo "- ${TARGET_SKILLS_DIR}/skill-creator/SKILL.md"

if [[ "${BACKED_UP}" -eq 1 ]]; then
  echo "Backup created at ${BACKUP_DIR}"
fi

sudo apt install npm -y
sudo npm install -g @openai/codex
