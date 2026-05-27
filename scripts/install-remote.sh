#!/usr/bin/env bash
set -euo pipefail

echo "install-remote.sh is kept for compatibility. Prefer scripts/install.sh."
curl -fsSL "https://raw.githubusercontent.com/${LUBAN_LOOP_REPO:-Zanetach/luban-loop}/${LUBAN_LOOP_REF:-main}/scripts/install.sh" | bash
