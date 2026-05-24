#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

test -f "$ROOT/skills/luban/SKILL.md"
test -f "$ROOT/skills/luban/scripts/discover_verify.py"
test -f "$ROOT/skills/luban/think/SKILL.md"
test -f "$ROOT/skills/luban/hunt/SKILL.md"
test -f "$ROOT/skills/luban/check/SKILL.md"
test -f "$ROOT/skills/luban/square/SKILL.md"
test -f "$ROOT/scripts/install.sh"
test -f "$ROOT/scripts/install-remote.sh"

python3 -m py_compile "$ROOT/skills/luban/scripts/discover_verify.py"
python3 -m py_compile "$ROOT/skills/luban/check/scripts/audit_signals.py"
bash -n "$ROOT/scripts/install.sh" "$ROOT/scripts/install-remote.sh" "$ROOT/scripts/verify.sh"

grep -q "name: luban" "$ROOT/skills/luban/SKILL.md"
grep -q "Luban Loop" "$ROOT/skills/luban/SKILL.md"
grep -q "Builder" "$ROOT/skills/luban/SKILL.md"
grep -q "Seal" "$ROOT/skills/luban/SKILL.md"
grep -q "name: think" "$ROOT/skills/luban/think/SKILL.md"
grep -q "name: hunt" "$ROOT/skills/luban/hunt/SKILL.md"
grep -q "name: check" "$ROOT/skills/luban/check/SKILL.md"
grep -q "name: square" "$ROOT/skills/luban/square/SKILL.md"

echo "Verification passed."
