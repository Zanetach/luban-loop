#!/usr/bin/env python3
"""Sync vendored Waza modules into the Luban skill.

The sync is intentionally allowlisted. Luban owns the top-level entrypoint,
installer, verification discovery, and Square integration; Waza owns the
nested specialist modules and shared rules.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = ROOT / "skills" / "luban" / ".upstream-waza.json"

DEFAULT_REPO = "https://github.com/tw93/Waza.git"
DEFAULT_REF = "main"

SYNC_MAP = {
    "skills/check": "skills/luban/check",
    "skills/design": "skills/luban/design",
    "skills/health": "skills/luban/health",
    "skills/hunt": "skills/luban/hunt",
    "skills/learn": "skills/luban/learn",
    "skills/read": "skills/luban/read",
    "skills/think": "skills/luban/think",
    "skills/write": "skills/luban/write",
    "rules": "skills/luban/rules",
}

PRESERVED_SURFACES = (
    "skills/luban/SKILL.md",
    "skills/luban/square",
    "skills/luban/scripts",
    "scripts/install.sh",
    "scripts/verify.sh",
)

LUBAN_ADAPTERS = {
    "skills/luban/check/SKILL.md": {
        "python3 <waza>/skills/check/scripts/audit_signals.py --root <project>": (
            "python3 <luban-skill-dir>/check/scripts/audit_signals.py --root <project>"
        ),
    },
    "skills/luban/check/scripts/audit_signals.py": {
        "Run as: python3 skills/check/scripts/audit_signals.py --root <path>": (
            "Run as: python3 skills/luban/check/scripts/audit_signals.py --root <path>"
        ),
    },
    "skills/luban/read/references/read-methods.md": {
        "${CLAUDE_SKILL_DIR:-~/.agents/skills/read}/scripts/fetch_feishu.py": (
            "${LUBAN_SKILL_DIR:-$HOME/.agents/skills/luban}/read/scripts/fetch_feishu.py"
        ),
        '${CLAUDE_SKILL_DIR:-$HOME/.agents/skills/read}/scripts/fetch_feishu.py': (
            '${LUBAN_SKILL_DIR:-$HOME/.agents/skills/luban}/read/scripts/fetch_feishu.py'
        ),
        '${CLAUDE_SKILL_DIR:-$HOME/.agents/skills/read}/scripts/fetch_weixin.py': (
            '${LUBAN_SKILL_DIR:-$HOME/.agents/skills/luban}/read/scripts/fetch_weixin.py'
        ),
    },
}

HEALTH_UPSTREAM_BLOCK = """# Resolve collect-data.sh from canonical locations (no personal home-dir paths).
HEALTH_SCRIPT="${CLAUDE_SKILL_DIR:+$CLAUDE_SKILL_DIR/scripts/collect-data.sh}"
if [ ! -f "${HEALTH_SCRIPT:-}" ]; then
  for candidate in \\
    "./skills/health/scripts/collect-data.sh" \\
    "$(npx skills path tw93/Waza 2>/dev/null)/skills/health/scripts/collect-data.sh"; do
    [ -f "$candidate" ] && HEALTH_SCRIPT="$candidate" && break
  done
fi
if [ ! -f "${HEALTH_SCRIPT:-}" ]; then
  echo "health collect-data.sh not found; set CLAUDE_SKILL_DIR or reinstall: npx skills add tw93/Waza -a claude-code -g -y"
  exit 1
fi
bash "$HEALTH_SCRIPT"
"""

HEALTH_LUBAN_BLOCK = """# Resolve collect-data.sh from Luban's nested skill layout.
HEALTH_SCRIPT="${LUBAN_SKILL_DIR:+$LUBAN_SKILL_DIR/health/scripts/collect-data.sh}"
if [ ! -f "${HEALTH_SCRIPT:-}" ]; then
  for candidate in \\
    "./skills/luban/health/scripts/collect-data.sh" \\
    "$HOME/.agents/skills/luban/health/scripts/collect-data.sh" \\
    "$HOME/.codex/skills/luban/health/scripts/collect-data.sh" \\
    "$HOME/.claude/skills/luban/health/scripts/collect-data.sh"; do
    [ -f "$candidate" ] && HEALTH_SCRIPT="$candidate" && break
  done
fi
if [ ! -f "${HEALTH_SCRIPT:-}" ]; then
  echo "health collect-data.sh not found; set LUBAN_SKILL_DIR or reinstall Luban Loop"
  exit 1
fi
bash "$HEALTH_SCRIPT"
"""


def run(cmd: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        sys.stderr.write(result.stderr or result.stdout)
        raise SystemExit(result.returncode)
    return result.stdout.strip()


def read_state() -> dict[str, str]:
    if not STATE_FILE.exists():
        return {}
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))


def resolve_remote_head(repo: str, ref: str) -> str:
    output = run(["git", "ls-remote", repo, ref])
    if not output:
        raise SystemExit(f"ERROR: no remote ref found for {repo} {ref}")
    return output.split()[0]


def clone_upstream(repo: str, ref: str, workdir: Path) -> Path:
    checkout = workdir / "waza"
    run(["git", "clone", "--quiet", "--depth", "1", "--branch", ref, repo, str(checkout)])
    return checkout


def copy_surface(src: Path, dst: Path) -> None:
    if not src.exists():
        raise SystemExit(f"ERROR: upstream surface missing: {src}")
    if dst.exists():
        if dst.is_dir():
            shutil.rmtree(dst)
        else:
            dst.unlink()
    if src.is_dir():
        shutil.copytree(src, dst)
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def current_diff() -> str:
    return run(["git", "status", "--short", "--", "skills/luban"], cwd=ROOT)


def ensure_preserved_surfaces() -> None:
    missing = [path for path in PRESERVED_SURFACES if not (ROOT / path).exists()]
    if missing:
        raise SystemExit("ERROR: preserved Luban surface missing: " + ", ".join(missing))


def write_state(repo: str, ref: str, commit: str) -> None:
    payload = {
        "repo": repo,
        "ref": ref,
        "commit": commit,
        "synced_at": date.today().isoformat(),
        "strategy": (
            "vendor Waza modules into skills/luban while preserving the Luban "
            "entrypoint, Square, installer, and verification scripts"
        ),
    }
    STATE_FILE.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def apply_luban_adapters() -> None:
    """Patch upstream Waza text that assumes top-level skill installation."""
    for relative_path, replacements in LUBAN_ADAPTERS.items():
        path = ROOT / relative_path
        text = path.read_text(encoding="utf-8")
        for old, new in replacements.items():
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")

    health_path = ROOT / "skills/luban/health/SKILL.md"
    text = health_path.read_text(encoding="utf-8")
    if HEALTH_UPSTREAM_BLOCK in text:
        text = text.replace(HEALTH_UPSTREAM_BLOCK, HEALTH_LUBAN_BLOCK)
    health_path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync bundled Waza modules into Luban.")
    parser.add_argument("--repo", default=None, help="Waza git repository URL")
    parser.add_argument("--ref", default=None, help="Waza branch or tag")
    parser.add_argument("--check", action="store_true", help="Only report whether upstream changed")
    parser.add_argument("--force", action="store_true", help="Sync even when the recorded commit is current")
    args = parser.parse_args()

    state = read_state()
    repo = args.repo or state.get("repo") or DEFAULT_REPO
    ref = args.ref or state.get("ref") or DEFAULT_REF
    previous_commit = state.get("commit")
    remote_commit = resolve_remote_head(repo, ref)

    if args.check:
        if previous_commit == remote_commit:
            print(f"OK: Waza already current at {remote_commit}")
            return 0
        print(f"UPDATE: Waza {ref} moved from {previous_commit or 'unknown'} to {remote_commit}")
        return 1

    if previous_commit == remote_commit and not args.force:
        print(f"OK: Waza already current at {remote_commit}")
        return 0

    ensure_preserved_surfaces()
    before = current_diff()

    with tempfile.TemporaryDirectory(prefix="luban-waza-sync-") as tmp:
        upstream = clone_upstream(repo, ref, Path(tmp))
        checked_out = run(["git", "rev-parse", "HEAD"], cwd=upstream)
        if checked_out != remote_commit:
            raise SystemExit(f"ERROR: cloned {checked_out}, expected {remote_commit}")

        for upstream_path, luban_path in SYNC_MAP.items():
            copy_surface(upstream / upstream_path, ROOT / luban_path)

    apply_luban_adapters()
    write_state(repo, ref, remote_commit)
    ensure_preserved_surfaces()

    after = current_diff()
    if before == after:
        print(f"OK: Waza already current at {remote_commit}")
    else:
        print(f"OK: synced Waza {ref} at {remote_commit}")
        print("OK: preserved Luban-owned surfaces:")
        for surface in PRESERVED_SURFACES:
            print(f"  - {surface}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
