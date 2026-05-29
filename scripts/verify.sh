#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

test -f "$ROOT/skills/luban/SKILL.md"
test -f "$ROOT/skills/luban/.upstream-waza.json"
test -f "$ROOT/skills/luban/scripts/discover_verify.py"
test -f "$ROOT/skills/luban/think/SKILL.md"
test -f "$ROOT/skills/luban/design/SKILL.md"
test -f "$ROOT/skills/luban/hunt/SKILL.md"
test -f "$ROOT/skills/luban/check/SKILL.md"
test -f "$ROOT/skills/luban/write/SKILL.md"
test -f "$ROOT/skills/luban/learn/SKILL.md"
test -f "$ROOT/skills/luban/read/SKILL.md"
test -f "$ROOT/skills/luban/health/SKILL.md"
test -f "$ROOT/skills/luban/square/SKILL.md"
test -f "$ROOT/skills/luban/square/.upstream-square.json"
test -f "$ROOT/skills/luban/rules/durable-context.md"
test -f "$ROOT/skills/luban/square/references/upstream/CLAUDE.md"
test -f "$ROOT/skills/luban/square/references/upstream/.cursor/rules/square.mdc"
test -f "$ROOT/scripts/install.sh"
test -f "$ROOT/scripts/install-remote.sh"
test -f "$ROOT/scripts/sync-waza.py"
test -f "$ROOT/scripts/sync-square.py"

python3 -m json.tool "$ROOT/skills/luban/.upstream-waza.json" >/dev/null
python3 -m json.tool "$ROOT/skills/luban/square/.upstream-square.json" >/dev/null
python3 -m py_compile "$ROOT/skills/luban/scripts/discover_verify.py"
python3 -m py_compile "$ROOT/scripts/sync-waza.py"
python3 -m py_compile "$ROOT/scripts/sync-square.py"
python3 -m py_compile "$ROOT/skills/luban/check/scripts/audit_signals.py"
python3 -m py_compile "$ROOT/skills/luban/health/scripts/check_agent_context.py"
python3 -m py_compile "$ROOT/skills/luban/health/scripts/check_doc_refs.py"
python3 -m py_compile "$ROOT/skills/luban/health/scripts/check_maintainability.py"
python3 -m py_compile "$ROOT/skills/luban/health/scripts/check_verifier_output.py"
python3 -m py_compile "$ROOT/skills/luban/read/scripts/fetch_feishu.py"
python3 -m py_compile "$ROOT/skills/luban/read/scripts/fetch_local.py"
python3 -m py_compile "$ROOT/skills/luban/read/scripts/fetch_weixin.py"
bash -n "$ROOT/scripts/install.sh" "$ROOT/scripts/install-remote.sh" "$ROOT/scripts/verify.sh"
bash -n "$ROOT/skills/luban/check/scripts/run-tests.sh"
bash -n "$ROOT/skills/luban/health/scripts/check-agent-context.sh"
bash -n "$ROOT/skills/luban/health/scripts/check-doc-refs.sh"
bash -n "$ROOT/skills/luban/health/scripts/check-maintainability.sh"
bash -n "$ROOT/skills/luban/health/scripts/check-verifier-output.sh"
bash -n "$ROOT/skills/luban/health/scripts/collect-data.sh"
bash -n "$ROOT/skills/luban/read/scripts/fetch.sh"

INSTALL_TMP="$(mktemp -d)"
cleanup() {
  rm -rf "$INSTALL_TMP"
}
trap cleanup EXIT

AGENTS_HOME="$INSTALL_TMP/agents" \
CODEX_HOME="$INSTALL_TMP/codex" \
CLAUDE_HOME="$INSTALL_TMP/claude" \
  bash "$ROOT/scripts/install.sh" >/dev/null

test -f "$INSTALL_TMP/agents/skills/luban/SKILL.md"
test -f "$INSTALL_TMP/agents/skills/luban/.upstream-waza.json"
test -f "$INSTALL_TMP/agents/skills/luban/square/.upstream-square.json"
test -f "$INSTALL_TMP/codex/skills/luban/SKILL.md"
test -f "$INSTALL_TMP/claude/skills/luban/SKILL.md"
test -f "$INSTALL_TMP/claude/skills/luban/think/SKILL.md"
test -f "$INSTALL_TMP/claude/skills/luban/check/SKILL.md"
test -f "$INSTALL_TMP/claude/skills/luban/square/SKILL.md"

grep -q "name: luban" "$ROOT/skills/luban/SKILL.md"
grep -q "Luban Loop" "$ROOT/skills/luban/SKILL.md"
grep -q "Builder" "$ROOT/skills/luban/SKILL.md"
grep -q "Project Mode Contract" "$ROOT/skills/luban/SKILL.md"
grep -q "module loops" "$ROOT/skills/luban/SKILL.md"
grep -q "Seal" "$ROOT/skills/luban/SKILL.md"
grep -q "name: think" "$ROOT/skills/luban/think/SKILL.md"
grep -q "name: design" "$ROOT/skills/luban/design/SKILL.md"
grep -q "name: hunt" "$ROOT/skills/luban/hunt/SKILL.md"
grep -q "name: check" "$ROOT/skills/luban/check/SKILL.md"
grep -q "name: write" "$ROOT/skills/luban/write/SKILL.md"
grep -q "name: learn" "$ROOT/skills/luban/learn/SKILL.md"
grep -q "name: read" "$ROOT/skills/luban/read/SKILL.md"
grep -q "name: health" "$ROOT/skills/luban/health/SKILL.md"
grep -q "name: square" "$ROOT/skills/luban/square/SKILL.md"

echo "Verification passed."
