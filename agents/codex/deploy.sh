#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_CONFIG="${SCRIPT_DIR}/config.toml"
SOURCE_AGENTS="${SCRIPT_DIR}/AGENTS.md"
TARGET_DIR="${HOME}/.codex"
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

echo "Codex files deployed to ${TARGET_DIR}"
echo "- ${TARGET_DIR}/config.toml"
echo "- ${TARGET_DIR}/AGENTS.md"

if [[ "${BACKED_UP}" -eq 1 ]]; then
  echo "Backup created at ${BACKUP_DIR}"
fi
