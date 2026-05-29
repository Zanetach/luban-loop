#!/usr/bin/env python3
"""Check Luban-owned semantic contracts that syntax tests cannot catch."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def require_contains(relative_path: str, needles: list[str]) -> list[str]:
    text = read(relative_path)
    missing = [needle for needle in needles if needle not in text]
    return [f"{relative_path}: missing `{needle}`" for needle in missing]


def require_regex(relative_path: str, pattern: str, description: str) -> list[str]:
    text = read(relative_path)
    if re.search(pattern, text, re.MULTILINE | re.DOTALL):
        return []
    return [f"{relative_path}: missing {description}"]


def require_absent(relative_path: str, needles: list[str]) -> list[str]:
    text = read(relative_path)
    found = [needle for needle in needles if needle in text]
    return [f"{relative_path}: leaked `{needle}`" for needle in found]


def main() -> int:
    errors: list[str] = []

    errors += require_contains(
        "skills/luban/SKILL.md",
        [
            "## Autonomy Contract",
            "continue automatically through Build -> Verify -> fix failures -> Verify again -> Check -> Seal",
            "## Project Mode Contract",
            "When the requirement implies a project-level result",
            "does not require the user to say \"from scratch\", \"from 0 to 1\", or \"project mode\"",
            "Project Mode applies both to new projects and to existing projects",
            "Project Mode goal: turn a requirement into a runnable, inspectable project result",
            "module loops",
            "Do not ask \"should I continue?\"",
            "## User Feedback Contract",
        ],
    )

    errors += require_contains(
        "scripts/sync-waza.py",
        [
            "\"skills/luban/SKILL.md\"",
            "\"skills/luban/square\"",
            "\"skills/luban/scripts\"",
            "\"scripts/install.sh\"",
            "\"scripts/verify.sh\"",
            "apply_luban_adapters",
            "HEALTH_LUBAN_BLOCK",
        ],
    )

    errors += require_contains(
        "scripts/sync-square.py",
        [
            "\"skills/luban/square/SKILL.md\"",
            "\"skills/luban/SKILL.md\"",
            "refresh Square upstream reference files while preserving Luban's Square skill entrypoint",
        ],
    )

    errors += require_contains(
        ".github/workflows/verify.yml",
        [
            "branches: [main]",
            "tags:",
            "\"v*\"",
            "./scripts/verify.sh",
        ],
    )

    errors += require_contains(
        ".github/workflows/sync-upstreams.yml",
        [
            "python3 scripts/sync-waza.py",
            "python3 scripts/sync-square.py",
            "./scripts/verify.sh",
            "peter-evans/create-pull-request",
            "gh pr merge",
        ],
    )

    errors += require_contains(
        "README.md",
        [
            "Luban Loop",
            "one top-level `luban` skill",
            "./scripts/verify.sh",
        ],
    )

    errors += require_contains(
        "docs/release.md",
        [
            "Stable: install from a tagged release.",
            "LUBAN_LOOP_REF",
            "Do not create a release tag from a dirty worktree.",
        ],
    )

    errors += require_regex(
        "VERSION",
        r"^\d+\.\d+\.\d+\n$",
        "semantic version in MAJOR.MINOR.PATCH form",
    )

    for public_path in (
        "README.md",
        "NOTICE.md",
        "docs/capability-review.md",
        "docs/summary.md",
        "skills/luban/SKILL.md",
    ):
        errors += require_absent(
            public_path,
            [
                "Waza",
                "waza",
                "tw93/Waza",
                "sync-waza.py",
                "sync-square.py",
                ".upstream-waza",
                ".upstream-square",
                "Maintain Bundles",
                "auto-merge",
            ],
        )

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("Semantic contract checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
