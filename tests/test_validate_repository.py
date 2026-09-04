"""Unit tests for the dependency-free repository validator."""

from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_repository", ROOT / "scripts/validate_repository.py"
)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class RepositoryValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name) / "repository"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(".git", "__pycache__"))

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def failures(self) -> list[str]:
        return VALIDATOR.validate_repository(self.root)

    def manifest(self) -> tuple[Path, dict]:
        path = self.root / "detections/tests/manifest.json"
        return path, json.loads(path.read_text(encoding="utf-8"))

    def write_manifest(self, path: Path, data: dict) -> None:
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    def test_current_repository_passes(self) -> None:
        self.assertEqual([], self.failures())

    def test_missing_rule_is_rejected(self) -> None:
        path, data = self.manifest()
        data["detections"] = data["detections"][:-1]
        self.write_manifest(path, data)
        self.assertTrue(any("rule IDs must be exactly" in item for item in self.failures()))

    def test_public_reproduction_requires_fixtures(self) -> None:
        path, data = self.manifest()
        data["detections"][0]["evidence_status"] = "reproduced-public"
        self.write_manifest(path, data)
        self.assertTrue(any("without fixtures/results" in item for item in self.failures()))

    def test_broken_internal_link_is_rejected(self) -> None:
        readme = self.root / "README.md"
        readme.write_text(
            readme.read_text(encoding="utf-8") + "\n[missing](docs/does-not-exist.md)\n",
            encoding="utf-8",
        )
        self.assertTrue(any("broken internal link" in item for item in self.failures()))

    def test_secret_pattern_is_rejected(self) -> None:
        sample = self.root / "examples/unsafe.md"
        sample.write_text("token: " + "AKIA" + "A" * 16 + "\n", encoding="utf-8")
        self.assertTrue(any("AWS access key" in item for item in self.failures()))


if __name__ == "__main__":
    unittest.main()
