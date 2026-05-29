#!/usr/bin/env python3
"""Behavior tests for Luban verification command discovery."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DISCOVER = ROOT / "skills" / "luban" / "scripts" / "discover_verify.py"


def run_discover(project: Path) -> dict:
    output = subprocess.check_output(
        ["python3", str(DISCOVER), "--root", str(project)],
        text=True,
    )
    return json.loads(output)


class DiscoverVerifyTests(unittest.TestCase):
    def test_reads_documented_verify_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "README.md").write_text(
                "# Demo\n\n## Verify\n\n```bash\n./scripts/verify.sh\n```\n",
                encoding="utf-8",
            )
            result = run_discover(project)

        self.assertIn("README.md", result["detected_files"])
        self.assertEqual(result["commands"][0]["command"], "./scripts/verify.sh")
        self.assertEqual(result["commands"][0]["confidence"], "high")
        self.assertEqual(result["commands"][0]["phase"], "verify")

    def test_discovers_package_scripts_with_lockfile_manager(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "package.json").write_text(
                json.dumps({"scripts": {"test": "vitest", "build": "vite build"}}),
                encoding="utf-8",
            )
            (project / "pnpm-lock.yaml").write_text("lockfileVersion: '9.0'\n", encoding="utf-8")
            result = run_discover(project)

        commands = [entry["command"] for entry in result["commands"]]
        self.assertIn("pnpm run test", commands)
        self.assertIn("pnpm run build", commands)
        self.assertIn("node", result["project_types"])

    def test_discovers_python_unittest_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "tests").mkdir()
            (project / "tests" / "test_example.py").write_text(
                "import unittest\n\nclass DemoTest(unittest.TestCase):\n    pass\n",
                encoding="utf-8",
            )
            result = run_discover(project)

        commands = [entry["command"] for entry in result["commands"]]
        self.assertIn("python3 -m unittest discover -s tests -v", commands)
        self.assertIn("tests/", result["detected_files"])


if __name__ == "__main__":
    unittest.main()
