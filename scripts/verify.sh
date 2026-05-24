#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

test -f "$ROOT/skills/deliver/SKILL.md"
test -f "$ROOT/skills/deliver/scripts/discover_verify.py"
test -f "$ROOT/scripts/install.sh"
test -f "$ROOT/scripts/install-remote.sh"

python3 -m py_compile "$ROOT/skills/deliver/scripts/discover_verify.py"
bash -n "$ROOT/scripts/install.sh" "$ROOT/scripts/install-remote.sh" "$ROOT/scripts/verify.sh"

grep -q "Luban Loop" "$ROOT/skills/deliver/SKILL.md"
grep -q "Builder" "$ROOT/skills/deliver/SKILL.md"
grep -q "Seal" "$ROOT/skills/deliver/SKILL.md"

echo "Verification passed."
