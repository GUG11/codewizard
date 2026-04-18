#!/usr/bin/env bash
set -euo pipefail

src_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
backup_dir="${HOME}/.rootdirs-backups/$(date +%Y%m%d_%H%M%S)"
backed_up=0

for src in "${src_dir}"/.*; do
  name="$(basename "${src}")"

  [[ "${name}" == "." || "${name}" == ".." ]] && continue

  dst="${HOME}/${name}"

  if [[ -e "${dst}" || -L "${dst}" ]]; then
    [[ "${backed_up}" -eq 0 ]] && mkdir -p "${backup_dir}"
    cp -R "${dst}" "${backup_dir}/${name}"
    backed_up=1
  fi

  cp -R "${src}" "${dst}"
  echo "Deployed ${dst}"
done

if [[ "${backed_up}" -eq 1 ]]; then
  echo "Backup created at ${backup_dir}"
fi
