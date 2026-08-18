#!/usr/bin/env python3
"""Validate the local Open NG-SOC staging skeleton without external dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = (
    "README.md",
    "CHANGELOG.md",
    "ROADMAP.md",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "CITATION.cff",
    "LICENSE-PENDING.md",
    ".gitattributes",
    ".gitignore",
    "detections/tests/manifest.yml",
    "docs/detections/coverage-matrix.md",
)

FORBIDDEN_SUFFIXES = {
    ".evtx", ".pcap", ".pcapng", ".vmdk", ".ova", ".ovf", ".iso",
    ".p12", ".pfx", ".key", ".pem", ".dump",
}

SECRET_PATTERNS = {
    "AWS access key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "Slack token": re.compile(r"xox[baprs]-[A-Za-z0-9-]+"),
    "GitHub token": re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}


def main() -> int:
    failures: list[str] = []

    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            failures.append(f"missing required file: {relative}")

    manifest_path = ROOT / "detections/tests/manifest.yml"
    if manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"manifest is not valid JSON-compatible YAML: {exc}")
        else:
            detections = manifest.get("detections", [])
            ids = [item.get("rule_id") for item in detections]
            if len(ids) != len(set(ids)):
                failures.append("manifest contains duplicate rule IDs")
            for item in detections:
                for field in (
                    "rule_id", "title", "release", "evidence_status",
                    "fixture_status", "expected_level", "mitre",
                ):
                    if field not in item:
                        failures.append(
                            f"rule {item.get('rule_id', '?')} missing field: {field}"
                        )

    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            failures.append(f"forbidden artifact type: {path.relative_to(ROOT)}")
            continue
        if path.suffix.lower() not in {
            ".md", ".py", ".yml", ".yaml", ".json", ".xml", ".cff",
            ".example", "",
        }:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            failures.append(f"non-UTF-8 text file: {path.relative_to(ROOT)}")
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(content):
                failures.append(f"possible {label} in {path.relative_to(ROOT)}")

    if failures:
        print("Repository validation failed:")
        for item in failures:
            print(f"- {item}")
        return 1

    print("Repository validation passed.")
    print("Note: this check does not replace credential rotation or a dedicated secret scanner.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
