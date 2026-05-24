#!/usr/bin/env python3
"""Discover project verification commands for the deliver skill."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any


DOC_NAMES = (
    "AGENTS.md",
    "CLAUDE.md",
    "README.md",
    "CONTRIBUTING.md",
    "DEVELOPMENT.md",
)
CI_DIRS = (".github/workflows", ".gitlab-ci.yml", ".circleci")
VERIFY_SCRIPT_NAMES = ("test", "qa", "qa:evidence", "e2e", "lint", "typecheck", "check", "build")
COMMAND_RE = re.compile(
    r"(?P<cmd>(?:python3?|pytest|uv|npm|npx|pnpm|yarn|bun|make|just|task|go|cargo|swift|xcodebuild|mvn|gradle|curl|./)[^\n`]*)",
    re.IGNORECASE,
)
COMMAND_START_RE = re.compile(
    r"^(?:[$>#]\s*)?(?P<cmd>(?:python3?|pytest|uv|npm|npx|pnpm|yarn|bun|make|just|task|go|cargo|swift|xcodebuild|mvn|gradle|curl|./)\b[^\n`]*)",
    re.IGNORECASE,
)
INLINE_CODE_RE = re.compile(r"`([^`]+)`")
VERIFY_WORD_RE = re.compile(
    r"\b(test|tests|pytest|unittest|qa|e2e|lint|typecheck|check|build|verify|validate|validation|ci)\b",
    re.IGNORECASE,
)


def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    for path in (current, *current.parents):
        if (path / ".git").exists():
            return path
        if any((path / name).exists() for name in ("package.json", "pyproject.toml", "Cargo.toml", "go.mod")):
            return path
    return current


def read_text(path: Path, limit: int = 200_000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")[:limit]
    except OSError:
        return ""


def add_command(
    commands: list[dict[str, Any]],
    seen: set[str],
    command: str,
    source: str,
    reason: str,
    confidence: str,
    phase: str,
) -> None:
    clean = " ".join(command.strip().split())
    clean = clean.rstrip(".,;")
    if not clean or clean in seen:
        return
    seen.add(clean)
    commands.append(
        {
            "command": clean,
            "source": source,
            "reason": reason,
            "confidence": confidence,
            "phase": phase,
        }
    )


def package_manager(root: Path) -> str:
    if (root / "pnpm-lock.yaml").exists():
        return "pnpm"
    if (root / "yarn.lock").exists():
        return "yarn"
    if (root / "bun.lockb").exists() or (root / "bun.lock").exists():
        return "bun"
    return "npm"


def scan_docs(root: Path, commands: list[dict[str, Any]], seen: set[str], detected: list[str]) -> None:
    for name in DOC_NAMES:
        path = root / name
        if not path.exists():
            continue
        detected.append(name)
        text = read_text(path)
        in_fence = False
        recent_verify_context = False
        pending_code_line = ""
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if line.startswith("```"):
                if pending_code_line:
                    add_doc_command(commands, seen, pending_code_line, name, "Project documentation code block mentions this verification command.")
                    pending_code_line = ""
                in_fence = not in_fence
                continue
            if not line:
                recent_verify_context = False
                continue
            if VERIFY_WORD_RE.search(line):
                recent_verify_context = True
            if in_fence:
                if pending_code_line:
                    line = f"{pending_code_line} {line}"
                    pending_code_line = ""
                if line.endswith("\\"):
                    pending_code_line = line[:-1].rstrip()
                    continue
                if recent_verify_context or VERIFY_WORD_RE.search(line):
                    add_doc_command(commands, seen, line, name, "Project documentation code block mentions this verification command.")
                continue
            if VERIFY_WORD_RE.search(line):
                for inline in INLINE_CODE_RE.findall(line):
                    add_doc_command(commands, seen, inline.strip(), name, "Project documentation inline code mentions this verification command.")
                add_doc_command(commands, seen, line.lstrip("-* "), name, "Project documentation mentions this verification command.")


def add_doc_command(
    commands: list[dict[str, Any]],
    seen: set[str],
    line: str,
    source: str,
    reason: str,
) -> None:
    match = COMMAND_START_RE.match(line)
    if not match:
        return
    cmd = match.group("cmd")
    add_command(commands, seen, cmd, source, reason, "high", classify_phase(cmd))


def scan_package_json(root: Path, commands: list[dict[str, Any]], seen: set[str], detected: list[str]) -> bool:
    path = root / "package.json"
    if not path.exists():
        return False
    detected.append("package.json")
    try:
        data = json.loads(read_text(path))
    except json.JSONDecodeError:
        return True
    scripts = data.get("scripts", {})
    if not isinstance(scripts, dict):
        return True
    pm = package_manager(root)
    for name in VERIFY_SCRIPT_NAMES:
        if name in scripts:
            add_command(
                commands,
                seen,
                f"{pm} run {name}" if pm != "npm" else f"npm run {name}",
                "package.json",
                f"package.json defines a `{name}` script.",
                "high",
                name,
            )
    return True


def scan_python(root: Path, commands: list[dict[str, Any]], seen: set[str], detected: list[str]) -> bool:
    has_python = False
    for name in ("pyproject.toml", "setup.cfg", "setup.py", "tox.ini", "pytest.ini"):
        if (root / name).exists():
            detected.append(name)
            has_python = True
    tests_dir = root / "tests"
    if tests_dir.exists():
        detected.append("tests/")
        has_python = True
    if not has_python:
        return False
    text = "\n".join(read_text(root / name) for name in ("pyproject.toml", "setup.cfg", "tox.ini", "pytest.ini"))
    if "pytest" in text.lower():
        add_command(commands, seen, "python3 -m pytest", "python config", "Python test config references pytest.", "medium", "test")
    elif tests_dir.exists():
        add_command(
            commands,
            seen,
            "python3 -m unittest discover -s tests -v",
            "tests/",
            "Python tests directory exists and no pytest config was found.",
            "medium",
            "test",
        )
    return True


def scan_make_task_files(root: Path, commands: list[dict[str, Any]], seen: set[str], detected: list[str]) -> None:
    for name, runner in (("Makefile", "make"), ("justfile", "just"), ("Taskfile.yml", "task"), ("Taskfile.yaml", "task")):
        path = root / name
        if not path.exists():
            continue
        detected.append(name)
        text = read_text(path)
        for target in VERIFY_SCRIPT_NAMES:
            if re.search(rf"^{re.escape(target)}\s*:", text, re.MULTILINE):
                add_command(
                    commands,
                    seen,
                    f"{runner} {target}",
                    name,
                    f"{name} defines a `{target}` target.",
                    "medium",
                    target,
                )


def scan_ci(root: Path, commands: list[dict[str, Any]], seen: set[str], detected: list[str]) -> None:
    for ci in CI_DIRS:
        path = root / ci
        if path.is_file():
            detected.append(ci)
            scan_ci_file(root, path, commands, seen)
        elif path.is_dir():
            detected.append(ci + "/")
            for file_path in sorted(path.rglob("*")):
                if file_path.is_file() and file_path.suffix in {".yml", ".yaml"}:
                    scan_ci_file(root, file_path, commands, seen)


def scan_ci_file(root: Path, path: Path, commands: list[dict[str, Any]], seen: set[str]) -> None:
    rel = str(path.relative_to(root))
    for line in read_text(path).splitlines():
        stripped = line.strip()
        if not stripped.startswith("run:") and not stripped.startswith("- run:"):
            continue
        if not VERIFY_WORD_RE.search(stripped):
            continue
        cmd = stripped.split("run:", 1)[1].strip().strip("\"'")
        add_command(commands, seen, cmd, rel, "CI runs this verification-related command.", "medium", classify_phase(cmd))


def classify_phase(command: str) -> str:
    lowered = command.lower()
    if "lint" in lowered:
        return "lint"
    if "typecheck" in lowered or "type-check" in lowered or "tsc" in lowered:
        return "typecheck"
    if "build" in lowered:
        return "build"
    if "qa" in lowered or "e2e" in lowered:
        return "qa"
    if "test" in lowered or "pytest" in lowered or "unittest" in lowered:
        return "test"
    if "check" in lowered:
        return "check"
    return "verify"


def detect_project_types(root: Path) -> list[str]:
    types: list[str] = []
    markers = {
        "node": "package.json",
        "python": "pyproject.toml",
        "rust": "Cargo.toml",
        "go": "go.mod",
        "swift": "Package.swift",
        "java": "pom.xml",
    }
    for label, marker in markers.items():
        if (root / marker).exists():
            types.append(label)
    if (root / "setup.py").exists() or (root / "requirements.txt").exists():
        if "python" not in types:
            types.append("python")
    return types


def main() -> int:
    parser = argparse.ArgumentParser(description="Discover verification commands for a repository.")
    parser.add_argument("--root", default=os.getcwd(), help="Repository root or a path inside it.")
    args = parser.parse_args()

    root = find_repo_root(Path(args.root))
    commands: list[dict[str, Any]] = []
    seen: set[str] = set()
    detected: list[str] = []

    scan_docs(root, commands, seen, detected)
    scan_package_json(root, commands, seen, detected)
    scan_python(root, commands, seen, detected)
    scan_make_task_files(root, commands, seen, detected)
    scan_ci(root, commands, seen, detected)

    result = {
        "root": str(root),
        "project_types": detect_project_types(root),
        "detected_files": sorted(set(detected)),
        "commands": commands,
        "notes": [
            "Prefer high-confidence documented commands.",
            "Medium-confidence commands are inferred from manifests, task files, CI, or language conventions.",
            "This script only inspects files; it does not modify the repository.",
        ],
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
