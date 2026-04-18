autoload -Uz colors && colors
setopt prompt_subst

if [[ -f "${HOME}/.zshrc.local" ]]; then
  source "${HOME}/.zshrc.local"
fi

git_prompt_info() {
  local branch repo root
  branch=$(git symbolic-ref --short HEAD 2>/dev/null || git rev-parse --short HEAD 2>/dev/null) || return
  root=$(git rev-parse --show-toplevel 2>/dev/null) || return
  repo=${root:t}
  print -n "%F{245}(%f%F{81}${repo}%f%F{245}:%f%F{120}${branch}%f%F{245})%f"
}

PROMPT=$'%F{39}%n%f %F{245}at%f %F{111}%~%f $(git_prompt_info) %F{45}›%f '
