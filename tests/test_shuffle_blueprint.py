"""Static safety and contract tests for the sanitized Shuffle blueprint."""

from __future__ import annotations

import ipaddress
import json
import unittest
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def walk_keys(value):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_keys(child)


class ShuffleBlueprintTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.blueprint = json.loads((ROOT / "integrations/shuffle/workflow-blueprint.json").read_text(encoding="utf-8"))
        cls.payload = json.loads((ROOT / "examples/payloads/wazuh-ssh-alert.json").read_text(encoding="utf-8"))

    def test_blueprint_has_required_paths(self) -> None:
        nodes = {node["id"] for node in self.blueprint["nodes"]}
        required = {"wazuh_webhook","misp_lookup","match_decision","notify_match","record_no_match","invalid_payload","enrichment_error"}
        self.assertTrue(required.issubset(nodes))
        for branch in self.blueprint["branches"]:
            self.assertIn(branch["from"], nodes)
            self.assertIn(branch["to"], nodes)

    def test_no_export_secret_reference_fields(self) -> None:
        prohibited = set(self.blueprint["prohibited_export_fields"])
        self.assertFalse(prohibited.intersection(walk_keys(self.blueprint)))

    def test_configuration_marks_secret_values(self) -> None:
        configuration = {item["name"]: item for item in self.blueprint["configuration"]}
        self.assertTrue(configuration["MISP_API_KEY"]["secret"])
        self.assertTrue(configuration["SLACK_DESTINATION"]["secret"])

    def test_example_payload_contract(self) -> None:
        payload = self.payload
        datetime.fromisoformat(payload["timestamp"].replace("Z", "+00:00"))
        self.assertRegex(payload["rule"]["id"], r"^[0-9]+$")
        self.assertIsInstance(payload["rule"]["level"], int)
        self.assertLessEqual(payload["rule"]["level"], 16)
        self.assertRegex(payload["agent"]["id"], r"^[0-9]{3}$")
        ipaddress.IPv4Address(payload["data"]["srcip"])


if __name__ == "__main__":
    unittest.main()
