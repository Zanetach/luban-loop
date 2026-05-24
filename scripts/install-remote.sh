#!/usr/bin/env bash
set -euo pipefail

REPO="${LUBAN_LOOP_REPO:-Zanetach/luban-loop}"
REF="${LUBAN_LOOP_REF:-main}"
ARCHIVE_URL="https://github.com/${REPO}/archive/${REF}.tar.gz"
TMP_DIR="$(mktemp -d)"

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

need_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

need_cmd curl
need_cmd tar

echo "Downloading Luban Loop from ${REPO}@${REF}..."
curl -fsSL "$ARCHIVE_URL" | tar -xz -C "$TMP_DIR"

ROOT="$(find "$TMP_DIR" -maxdepth 1 -type d -name "*luban-loop*" | head -n 1)"
if [[ -z "$ROOT" || ! -f "$ROOT/scripts/install.sh" ]]; then
  echo "Could not find Luban Loop installer in downloaded archive." >&2
  exit 1
fi

bash "$ROOT/scripts/install.sh"
