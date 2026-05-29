#!/usr/bin/env bash
set -euo pipefail

REPO="${LUBAN_LOOP_REPO:-Zanetach/luban-loop}"
REF="${LUBAN_LOOP_REF:-main}"

if [[ -t 1 && -z "${NO_COLOR:-}" ]]; then
  BOLD="$(printf '\033[1m')"
  DIM="$(printf '\033[2m')"
  CYAN="$(printf '\033[36m')"
  GREEN="$(printf '\033[32m')"
  RESET="$(printf '\033[0m')"
else
  BOLD=""
  DIM=""
  CYAN=""
  GREEN=""
  RESET=""
fi

need_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

resolve_local_root() {
  local source="${BASH_SOURCE[0]:-$0}"
  local root
  root="$(cd "$(dirname "$source")/.." 2>/dev/null && pwd -P || true)"

  if [[ -n "$root" && -f "$root/skills/luban/SKILL.md" ]]; then
    printf '%s\n' "$root"
    return 0
  fi

  return 1
}

bootstrap_from_github() {
  need_cmd curl
  need_cmd tar

  local archive_url="https://github.com/${REPO}/archive/${REF}.tar.gz"
  local tmp_dir
  tmp_dir="$(mktemp -d)"

  cleanup() {
    rm -rf "${tmp_dir:-}"
  }
  trap cleanup EXIT

  echo "${CYAN}==>${RESET} Downloading ${BOLD}Luban Loop${RESET} from ${REPO}@${REF}"
  curl -fsSL "$archive_url" | tar -xz -C "$tmp_dir"

  local root
  root="$(find "$tmp_dir" -maxdepth 3 -type f -path "*/scripts/install.sh" -print -quit)"
  root="$(cd "$(dirname "$root")/.." 2>/dev/null && pwd -P || true)"
  if [[ -z "$root" || ! -f "$root/scripts/install.sh" ]]; then
    echo "Could not find Luban Loop installer in downloaded archive." >&2
    exit 1
  fi

  LUBAN_LOOP_BOOTSTRAPPED=1 bash "$root/scripts/install.sh"
}

print_logo() {
  printf '%s' "$CYAN"
  cat <<'EOF'
  _          _                  _
 | |   _   _| |__   __ _ _ __  | |    ___   ___  _ __
 | |  | | | | '_ \ / _` | '_ \ | |   / _ \ / _ \| '_ \
 | |__| |_| | |_) | (_| | | | || |__| (_) | (_) | |_) |
 |_____\__,_|_.__/ \__,_|_| |_||_____\___/ \___/| .__/
                                                |_|
EOF
  printf '%s' "$RESET"
}

if ! ROOT="$(resolve_local_root)"; then
  if [[ "${LUBAN_LOOP_BOOTSTRAPPED:-}" == "1" ]]; then
    echo "Could not find skills/luban next to the installer." >&2
    exit 1
  fi

  bootstrap_from_github
  exit 0
fi

print_logo
echo "${CYAN}==>${RESET} Installing ${BOLD}Luban Loop${RESET} from ${DIM}$ROOT${RESET}"

install_skill() {
  local target="$1"
  mkdir -p "$target"
  rm -rf "$target/luban"
  cp -R "$ROOT/skills/luban" "$target/luban"
  echo "    ${GREEN}installed:${RESET} $target/luban"

  for legacy in think design hunt check write learn read health square; do
    if [[ -f "$target/$legacy/SKILL.md" ]] && [[ -f "$ROOT/skills/luban/$legacy/SKILL.md" ]] && cmp -s "$target/$legacy/SKILL.md" "$ROOT/skills/luban/$legacy/SKILL.md"; then
      rm -rf "$target/$legacy"
      echo "    ${DIM}removed legacy module:${RESET} $target/$legacy"
    fi
  done

  if [[ -f "$target/karpathy-guidelines/SKILL.md" ]] && grep -q "Karpathy Guidelines\\|Square" "$target/karpathy-guidelines/SKILL.md"; then
    rm -rf "$target/karpathy-guidelines"
    echo "    ${DIM}removed legacy Square skill:${RESET} $target/karpathy-guidelines"
  fi

  if [[ -f "$target/deliver/SKILL.md" ]] && grep -q "Luban Loop" "$target/deliver/SKILL.md"; then
    rm -rf "$target/deliver"
    echo "    ${DIM}removed legacy Luban skill:${RESET} $target/deliver"
  fi
}

install_skill "${AGENTS_HOME:-$HOME/.agents}/skills"
install_skill "${CODEX_HOME:-$HOME/.codex}/skills"
install_skill "${CLAUDE_HOME:-$HOME/.claude}/skills"

cat <<EOF

${CYAN}==>${RESET} ${GREEN}Luban Loop installed${RESET}

Use it in Claude Code:
  /luban <requirement>

Or ask naturally:
  Use Luban to implement: <requirement>
  用 Luban 实现：<需求>

Luban process:
  Requirement -> Builder -> Chalkline -> Square -> Build -> Rootfinder -> Verify -> Gauge -> Seal

If Claude Code was already running before installation, restart it if /luban is not listed yet.
EOF
