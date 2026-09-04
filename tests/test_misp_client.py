"""Synthetic, network-free tests for the public MISP client."""

from __future__ import annotations

import importlib.util
import json
import socket
import sys
import unittest
from pathlib import Path
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("misp_client", ROOT / "integrations/misp/client.py")
assert SPEC and SPEC.loader
CLIENT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CLIENT
SPEC.loader.exec_module(CLIENT)


class Response:
    def __init__(self, body: bytes) -> None:
        self.body = body
    def __enter__(self):
        return self
    def __exit__(self, *_args):
        return False
    def read(self, _limit: int) -> bytes:
        return self.body


class MispClientTests(unittest.TestCase):
    def config(self, retries: int = 0):
        return CLIENT.Config("https://misp.example", "test-key-not-a-real-secret", max_retries=retries)

    def test_match(self) -> None:
        body = json.dumps({"response":{"Attribute":[{"type":"ip-src","value":"198.51.100.42","category":"Network activity","to_ids":True}]}}).encode()
        result = CLIENT.MispClient(self.config(), transport=lambda *_a, **_k: Response(body)).search("ip", "198.51.100.42")
        self.assertTrue(result["misp_match"])
        self.assertEqual(1, result["match_count"])

    def test_no_match(self) -> None:
        body = b'{"response":{"Attribute":[]}}'
        result = CLIENT.MispClient(self.config(), transport=lambda *_a, **_k: Response(body)).search("domain", "safe.example")
        self.assertFalse(result["misp_match"])

    def test_timeout_is_safely_reported(self) -> None:
        def timeout(*_args, **_kwargs):
            raise socket.timeout()
        with self.assertRaisesRegex(CLIENT.MispError, "timeout"):
            CLIENT.MispClient(self.config(), transport=timeout).search("ip", "192.0.2.1")

    def test_invalid_json_is_rejected(self) -> None:
        with self.assertRaisesRegex(CLIENT.MispError, "invalid JSON"):
            CLIENT.MispClient(self.config(), transport=lambda *_a, **_k: Response(b"not-json")).search("ip", "192.0.2.1")

    def test_server_error_retries_then_fails(self) -> None:
        calls = []
        def server_error(request, **_kwargs):
            calls.append(request)
            raise HTTPError(request.full_url, 503, "unavailable", {}, None)
        with self.assertRaisesRegex(CLIENT.MispError, "503"):
            CLIENT.MispClient(self.config(1), transport=server_error, sleeper=lambda _n: None).search("ip", "192.0.2.1")
        self.assertEqual(2, len(calls))

    def test_invalid_ioc_is_rejected_before_network(self) -> None:
        with self.assertRaisesRegex(CLIENT.MispError, "invalid IP"):
            CLIENT.MispClient(self.config(), transport=lambda *_a, **_k: self.fail("network called")).search("ip", "999.1.1.1")


if __name__ == "__main__":
    unittest.main()
