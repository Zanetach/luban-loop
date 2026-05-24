#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

install_skill() {
  local target="$1"
  mkdir -p "$target"
  for skill in luban think hunt check karpathy-guidelines; do
    rm -rf "$target/$skill"
    cp -R "$ROOT/skills/$skill" "$target/$skill"
    echo "Installed $skill skill to $target/$skill"
  done

  if [[ -f "$target/deliver/SKILL.md" ]] && grep -q "Luban Loop" "$target/deliver/SKILL.md"; then
    rm -rf "$target/deliver"
    echo "Removed legacy Luban Loop install at $target/deliver"
  fi
}

install_skill "${AGENTS_HOME:-$HOME/.agents}/skills"
install_skill "${CODEX_HOME:-$HOME/.codex}/skills"

echo "Luban Loop installed. Try: Use Luban to implement: <requirement>"
