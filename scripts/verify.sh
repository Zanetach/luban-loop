#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

test -f "$ROOT/skills/luban/SKILL.md"
test -f "$ROOT/skills/luban/scripts/discover_verify.py"
test -f "$ROOT/skills/think/SKILL.md"
test -f "$ROOT/skills/hunt/SKILL.md"
test -f "$ROOT/skills/check/SKILL.md"
test -f "$ROOT/skills/square/SKILL.md"
test -f "$ROOT/scripts/install.sh"
test -f "$ROOT/scripts/install-remote.sh"

python3 -m py_compile "$ROOT/skills/luban/scripts/discover_verify.py"
python3 -m py_compile "$ROOT/skills/check/scripts/audit_signals.py"
bash -n "$ROOT/scripts/install.sh" "$ROOT/scripts/install-remote.sh" "$ROOT/scripts/verify.sh"

grep -q "name: luban" "$ROOT/skills/luban/SKILL.md"
grep -q "Luban Loop" "$ROOT/skills/luban/SKILL.md"
grep -q "Builder" "$ROOT/skills/luban/SKILL.md"
grep -q "Seal" "$ROOT/skills/luban/SKILL.md"
grep -q "name: think" "$ROOT/skills/think/SKILL.md"
grep -q "name: hunt" "$ROOT/skills/hunt/SKILL.md"
grep -q "name: check" "$ROOT/skills/check/SKILL.md"
grep -q "name: square" "$ROOT/skills/square/SKILL.md"

echo "Verification passed."
