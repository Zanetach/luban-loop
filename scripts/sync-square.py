#!/usr/bin/env python3
"""Refresh Square's bundled upstream reference files.

This keeps the upstream distribution material current without replacing
Luban's own `skills/luban/square/SKILL.md` entrypoint.
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
STATE_FILE = ROOT / "skills" / "luban" / "square" / ".upstream-square.json"
UPSTREAM_DIR = ROOT / "skills" / "luban" / "square" / "references" / "upstream"

DEFAULT_REPO = "https://github.com/multica-ai/andrej-karpathy-skills.git"
DEFAULT_REF = "main"

FILE_MAP = {
    "CLAUDE.md": "CLAUDE.md",
    "CURSOR.md": "CURSOR.md",
    "EXAMPLES.md": "EXAMPLES.md",
    "README.md": "README.md",
    "README.zh.md": "README.zh.md",
    ".cursor/rules/karpathy-guidelines.mdc": ".cursor/rules/square.mdc",
}

DIR_MAP = {
    ".claude-plugin": ".claude-plugin",
}

PRESERVED_SURFACES = (
    "skills/luban/square/SKILL.md",
    "skills/luban/SKILL.md",
)


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
    checkout = workdir / "square"
    run(["git", "clone", "--quiet", "--depth", "1", "--branch", ref, repo, str(checkout)])
    return checkout


def copy_file(src: Path, dst: Path) -> None:
    if not src.is_file():
        raise SystemExit(f"ERROR: upstream file missing: {src}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def copy_dir(src: Path, dst: Path) -> None:
    if not src.is_dir():
        raise SystemExit(f"ERROR: upstream directory missing: {src}")
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


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
        "strategy": "refresh Square upstream reference files while preserving Luban's Square skill entrypoint",
    }
    STATE_FILE.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh bundled Square upstream references.")
    parser.add_argument("--repo", default=None, help="Upstream git repository URL")
    parser.add_argument("--ref", default=None, help="Upstream branch or tag")
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
            print(f"OK: Square upstream already current at {remote_commit}")
            return 0
        print(f"UPDATE: Square upstream {ref} moved from {previous_commit or 'unknown'} to {remote_commit}")
        return 1

    if previous_commit == remote_commit and not args.force:
        print(f"OK: Square upstream already current at {remote_commit}")
        return 0

    ensure_preserved_surfaces()

    with tempfile.TemporaryDirectory(prefix="luban-square-sync-") as tmp:
        upstream = clone_upstream(repo, ref, Path(tmp))
        checked_out = run(["git", "rev-parse", "HEAD"], cwd=upstream)
        if checked_out != remote_commit:
            raise SystemExit(f"ERROR: cloned {checked_out}, expected {remote_commit}")

        for upstream_path, luban_path in FILE_MAP.items():
            copy_file(upstream / upstream_path, UPSTREAM_DIR / luban_path)
        for upstream_path, luban_path in DIR_MAP.items():
            copy_dir(upstream / upstream_path, UPSTREAM_DIR / luban_path)

    write_state(repo, ref, remote_commit)
    ensure_preserved_surfaces()
    print(f"OK: refreshed Square upstream {ref} at {remote_commit}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
