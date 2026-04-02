#!/usr/bin/env bash
# run: bash agents/codex/deploy.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_CONFIG="${SCRIPT_DIR}/config.toml"
SOURCE_AGENTS="${SCRIPT_DIR}/AGENTS.md"
SOURCE_MODES_DIR="${SCRIPT_DIR}/modes"
SOURCE_SKILLS_DIR="${SCRIPT_DIR}/skills"
TARGET_DIR="${HOME}/.codex"
TARGET_MODES_DIR="${TARGET_DIR}/modes"
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

if [[ ! -d "${SOURCE_MODES_DIR}" ]]; then
  echo "Error: missing source directory: ${SOURCE_MODES_DIR}" >&2
  exit 1
fi

if [[ ! -d "${SOURCE_SKILLS_DIR}" ]]; then
  echo "Error: missing source directory: ${SOURCE_SKILLS_DIR}" >&2
  exit 1
fi

mkdir -p "${TARGET_DIR}"
mkdir -p "${TARGET_MODES_DIR}"
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
cp -a "${SOURCE_MODES_DIR}/." "${TARGET_MODES_DIR}/"
cp -a "${SOURCE_SKILLS_DIR}/." "${TARGET_SKILLS_DIR}/"

echo "Codex files deployed to ${TARGET_DIR}"
echo "- ${TARGET_DIR}/config.toml"
echo "- ${TARGET_DIR}/AGENTS.md"
echo "- ${TARGET_MODES_DIR}"
echo "- ${TARGET_SKILLS_DIR}"

if [[ "${BACKED_UP}" -eq 1 ]]; then
  echo "Backup created at ${BACKUP_DIR}"
fi

sudo apt install npm -y
sudo npm install -g @openai/codex
