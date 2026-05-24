#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

test -f "$ROOT/skills/deliver/SKILL.md"
test -f "$ROOT/skills/deliver/scripts/discover_verify.py"

python3 -m py_compile "$ROOT/skills/deliver/scripts/discover_verify.py"

grep -q "Luban Loop" "$ROOT/skills/deliver/SKILL.md"
grep -q "Builder" "$ROOT/skills/deliver/SKILL.md"
grep -q "Seal" "$ROOT/skills/deliver/SKILL.md"

echo "Verification passed."
