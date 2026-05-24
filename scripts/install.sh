#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

install_skill() {
  local target="$1"
  mkdir -p "$target"
  rm -rf "$target/luban"
  cp -R "$ROOT/skills/luban" "$target/luban"
  echo "Installed luban skill to $target/luban"

  for legacy in think design hunt check write learn read health square; do
    if [[ -f "$target/$legacy/SKILL.md" ]] && [[ -f "$ROOT/skills/luban/$legacy/SKILL.md" ]] && cmp -s "$target/$legacy/SKILL.md" "$ROOT/skills/luban/$legacy/SKILL.md"; then
      rm -rf "$target/$legacy"
      echo "Removed legacy Luban module install at $target/$legacy"
    fi
  done

  if [[ -f "$target/karpathy-guidelines/SKILL.md" ]] && grep -q "Karpathy Guidelines\\|Square" "$target/karpathy-guidelines/SKILL.md"; then
    rm -rf "$target/karpathy-guidelines"
    echo "Removed legacy Square install at $target/karpathy-guidelines"
  fi

  if [[ -f "$target/deliver/SKILL.md" ]] && grep -q "Luban Loop" "$target/deliver/SKILL.md"; then
    rm -rf "$target/deliver"
    echo "Removed legacy Luban Loop install at $target/deliver"
  fi
}

install_skill "${AGENTS_HOME:-$HOME/.agents}/skills"
install_skill "${CODEX_HOME:-$HOME/.codex}/skills"

echo "Luban Loop installed. Try: Use Luban to implement: <requirement>"
