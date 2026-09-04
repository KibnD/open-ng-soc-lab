#!/usr/bin/env python3
"""Dependency-free static publication checks for Open NG-SOC Lab.

This validator does not execute Wazuh or replace credential rotation and a
dedicated history-aware secret scanner.
"""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_RULE_IDS = {*range(100051, 100060), 100100}
EVIDENCE_STATES = {
    "implemented-private", "tested-private", "reproduced-public",
    "documented-only", "simulated", "target",
}
REQUIRED_FILES = (
    "README.md", "README.fr.md", "REPOSITORY_STATUS.md", "CHANGELOG.md",
    "ROADMAP.md", "SECURITY.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md",
    "SUPPORT.md", ".github/CODEOWNERS", ".github/REPOSITORY_SETTINGS.md",
    "CITATION.cff", "LICENSE-PENDING.md", ".gitattributes", ".gitignore",
    "detections/tests/manifest.json",
    "detections/tests/schema/manifest.schema.json",
    ".github/workflows/ci.yml", ".github/dependabot.yml",
    "docs/detections/coverage-matrix.md", "docs/evidence/evidence-policy.md",
    "docs/LAB_EXPORT_CHECKLIST.md",
    "docs/deployment/wazuh.md", "docs/deployment/pfsense-suricata.md",
    "docs/deployment/misp.md", "docs/deployment/shuffle.md",
    "docs/troubleshooting/known-issues.md", "infrastructure/README.md",
    "integrations/misp/client.py", "integrations/misp/enrich.py",
    "integrations/misp/README.md", "tests/test_misp_client.py",
    "integrations/shuffle/workflow-blueprint.json",
    "integrations/shuffle/wazuh-alert.schema.json",
    "integrations/shuffle/README.md", "integrations/slack/message-template.json",
    "examples/payloads/wazuh-ssh-alert.json", "tests/test_shuffle_blueprint.py",
    "detections/wazuh/VERSION_SUPPORT.md", "docs/project/versioning.md",
    "docs/project/release-checklist.md",
    "docs/use-cases.md", "docs/assets/README.md", "dashboards/README.md",
    "simulations/safety-and-cleanup.md", "simulations/synthetic-cloudtrail.md",
    "simulations/ad-identity.md", "simulations/docker-privileged.md",
    "simulations/network-replay.md",
    *(f"docs/case-studies/pt-{number:02}.md" for number in range(1, 7)),
)
FORBIDDEN_SUFFIXES = {
    ".evtx", ".pcap", ".pcapng", ".vmdk", ".ova", ".ovf", ".iso",
    ".p12", ".pfx", ".key", ".pem", ".dump", ".dmp",
}
TEXT_SUFFIXES = {
    ".md", ".py", ".ps1", ".yml", ".yaml", ".json", ".xml", ".cff",
    ".example", ".gitignore", ".gitattributes", ".editorconfig", "",
}
SECRET_PATTERNS = {
    "AWS access key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "Slack token": re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    "GitHub token": re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    "generic webhook secret": re.compile(r"hooks\.slack\.com/services/[A-Za-z0-9/_-]+"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^]]+\]\(([^)]+)\)")
MITRE_ID = re.compile(r"^T[0-9]{4}(?:\.[0-9]{3})?$")


def _text_files(root: Path) -> list[Path]:
    return [
        path for path in root.rglob("*")
        if path.is_file() and not {".git", "__pycache__", ".pytest_cache"}.intersection(path.parts)
        and (path.suffix.lower() in TEXT_SUFFIXES or path.name in TEXT_SUFFIXES)
    ]


def validate_repository(root: Path) -> list[str]:
    """Return every validation failure found under *root*."""
    failures: list[str] = []
    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            failures.append(f"missing required file: {relative}")

    manifest_path = root / "detections/tests/manifest.json"
    manifest: dict = {}
    if manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            failures.append(f"manifest is not valid UTF-8 JSON: {exc}")

    detections = manifest.get("detections", []) if isinstance(manifest, dict) else []
    if not isinstance(detections, list):
        failures.append("manifest detections must be an array")
        detections = []
    ids = [item.get("rule_id") for item in detections if isinstance(item, dict)]
    if set(ids) != REQUIRED_RULE_IDS:
        failures.append("manifest rule IDs must be exactly 100051-100059 and 100100")
    if len(ids) != len(set(ids)):
        failures.append("manifest contains duplicate rule IDs")

    required_fields = {
        "rule_id", "title", "data_source", "prerequisites", "expected_decoder",
        "expected_level", "mitre", "mitre_justification", "evidence_status",
        "positive_fixture", "negative_fixture", "expected_result",
        "release_target", "cleanup", "limitations",
    }
    for item in detections:
        if not isinstance(item, dict):
            failures.append("manifest detection entries must be objects")
            continue
        rule_id = item.get("rule_id", "?")
        missing = required_fields - item.keys()
        for field in sorted(missing):
            failures.append(f"rule {rule_id} missing field: {field}")
        if item.get("evidence_status") not in EVIDENCE_STATES:
            failures.append(f"rule {rule_id} has invalid evidence status")
        level = item.get("expected_level")
        if not isinstance(level, int) or not 0 <= level <= 16:
            failures.append(f"rule {rule_id} has invalid expected level")
        mitre = item.get("mitre")
        if not isinstance(mitre, list) or any(not MITRE_ID.fullmatch(x) for x in mitre):
            failures.append(f"rule {rule_id} has invalid MITRE mapping")
        if not (root / f"docs/detections/rule-{rule_id}.md").is_file():
            failures.append(f"rule {rule_id} missing detection documentation")
        for field in ("positive_fixture", "negative_fixture", "expected_result"):
            relative = item.get(field)
            if relative and not (root / relative).is_file():
                failures.append(f"rule {rule_id} references missing {field}: {relative}")
        if item.get("evidence_status") == "reproduced-public" and not all(
            item.get(field) for field in ("positive_fixture", "negative_fixture", "expected_result")
        ):
            failures.append(f"rule {rule_id} claims public reproduction without fixtures/results")

    xml_rule_ids: list[int] = []
    for path in root.rglob("*"):
        if not path.is_file() or {".git", "__pycache__", ".pytest_cache"}.intersection(path.parts):
            continue
        relative = path.relative_to(root)
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            failures.append(f"forbidden artifact type: {relative}")
        if path.suffix.lower() == ".xml":
            try:
                tree = ET.parse(path)
                for rule in tree.findall(".//rule[@id]"):
                    try:
                        xml_rule_ids.append(int(rule.attrib["id"]))
                    except ValueError:
                        failures.append(f"non-numeric XML rule ID in {relative}")
            except ET.ParseError as exc:
                failures.append(f"malformed XML in {relative}: {exc}")
        if path.suffix.lower() == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                failures.append(f"invalid JSON in {relative}: {exc}")
    if len(xml_rule_ids) != len(set(xml_rule_ids)):
        failures.append("Wazuh XML contains duplicate rule IDs")
    unknown_xml_ids = set(xml_rule_ids) - REQUIRED_RULE_IDS
    if unknown_xml_ids:
        failures.append(f"Wazuh XML contains IDs absent from manifest: {sorted(unknown_xml_ids)}")

    for path in _text_files(root):
        relative = path.relative_to(root)
        try:
            raw = path.read_bytes()
            content = raw.decode("utf-8")
        except UnicodeDecodeError:
            failures.append(f"non-UTF-8 text file: {relative}")
            continue
        if raw.startswith(b"\xef\xbb\xbf"):
            failures.append(f"UTF-8 BOM is not allowed: {relative}")
        if b"\r\n" in raw:
            failures.append(f"CRLF line endings are not allowed: {relative}")
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(content):
                failures.append(f"possible {label} in {relative}")
        if path.suffix.lower() == ".md":
            for target in MARKDOWN_LINK.findall(content):
                target = target.strip().split(maxsplit=1)[0].strip("<>")
                if not target or target.startswith(("#", "https://", "http://", "mailto:")):
                    continue
                local = unquote(target.split("#", 1)[0])
                if local and not (path.parent / local).resolve().exists():
                    failures.append(f"broken internal link in {relative}: {target}")

    citation = root / "CITATION.cff"
    if citation.is_file():
        value = citation.read_text(encoding="utf-8")
        for key in ("cff-version:", "message:", "title:", "type:", "authors:"):
            if not re.search(rf"(?m)^{re.escape(key)}", value):
                failures.append(f"CITATION.cff missing required key: {key[:-1]}")
    return failures


def main() -> int:
    failures = validate_repository(ROOT)
    if failures:
        print("Repository validation failed:")
        for item in failures:
            print(f"- {item}")
        return 1
    print("Repository validation passed.")
    print("Scope: static publication checks only; Wazuh was not executed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
