#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

install_skill() {
  local target="$1"
  mkdir -p "$target"
  rm -rf "$target/deliver"
  cp -R "$ROOT/skills/deliver" "$target/deliver"
  echo "Installed deliver skill to $target/deliver"
}

install_skill "${AGENTS_HOME:-$HOME/.agents}/skills"
install_skill "${CODEX_HOME:-$HOME/.codex}/skills"

echo "Luban Loop installed. Try: Use Luban to implement: <requirement>"
