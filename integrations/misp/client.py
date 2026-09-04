#!/usr/bin/env python3
"""Small, safe-by-default MISP attribute lookup client.

This is a clean-room public adapter, not an export of the private lab script.
It returns enrichment data to the caller and never writes to a Wazuh queue.
"""

from __future__ import annotations

import ipaddress
import json
import os
import re
import socket
import ssl
import time
from dataclasses import dataclass
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

DOMAIN = re.compile(r"(?=^.{1,253}$)(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,63}$")
HASHES = {"md5": 32, "sha1": 40, "sha256": 64}
RETRYABLE_STATUS = {429, 502, 503, 504}


class MispError(RuntimeError):
    """Safe public error without credentials or response bodies."""


@dataclass(frozen=True)
class Config:
    url: str
    api_key: str
    ca_bundle: str | None = None
    connect_timeout: float = 3.0
    read_timeout: float = 7.0
    max_retries: int = 2

    @classmethod
    def from_environment(cls) -> "Config":
        url = os.environ.get("MISP_URL", "").rstrip("/")
        key = os.environ.get("MISP_API_KEY", "")
        if not url or not key:
            raise MispError("MISP_URL and MISP_API_KEY are required")
        parsed = urlparse(url)
        allow_http = os.environ.get("MISP_ALLOW_INSECURE_HTTP") == "1"
        if parsed.scheme != "https" and not (allow_http and parsed.scheme == "http"):
            raise MispError("MISP_URL must use HTTPS (lab HTTP requires explicit opt-in)")
        if not parsed.hostname or parsed.username or parsed.password:
            raise MispError("MISP_URL must be an absolute URL without embedded credentials")
        try:
            connect = float(os.environ.get("MISP_CONNECT_TIMEOUT", "3"))
            read = float(os.environ.get("MISP_READ_TIMEOUT", "7"))
            retries = int(os.environ.get("MISP_MAX_RETRIES", "2"))
        except ValueError as exc:
            raise MispError("MISP timeout/retry settings must be numeric") from exc
        if connect <= 0 or read <= 0 or not 0 <= retries <= 5:
            raise MispError("MISP timeouts must be positive and retries must be 0-5")
        return cls(url, key, os.environ.get("MISP_CA_BUNDLE") or None, connect, read, retries)


def normalize_ioc(ioc_type: str, value: str) -> tuple[list[str], str]:
    """Validate an IOC and return MISP attribute types plus normalized value."""
    kind = ioc_type.strip().lower()
    candidate = value.strip()
    if kind in {"ip", "ip-src", "ip-dst"}:
        try:
            candidate = str(ipaddress.ip_address(candidate))
        except ValueError as exc:
            raise MispError("invalid IP address") from exc
        types = [kind] if kind != "ip" else ["ip-src", "ip-dst"]
    elif kind == "domain":
        candidate = candidate.rstrip(".").lower()
        if not DOMAIN.fullmatch(candidate):
            raise MispError("invalid domain")
        types = ["domain"]
    elif kind in HASHES:
        candidate = candidate.lower()
        if len(candidate) != HASHES[kind] or not re.fullmatch(r"[0-9a-f]+", candidate):
            raise MispError(f"invalid {kind} value")
        types = [kind]
    else:
        raise MispError("unsupported IOC type")
    return types, candidate


class MispClient:
    def __init__(
        self,
        config: Config,
        transport: Callable[..., Any] = urlopen,
        sleeper: Callable[[float], None] = time.sleep,
    ) -> None:
        self.config = config
        self.transport = transport
        self.sleeper = sleeper
        self.context = ssl.create_default_context(cafile=config.ca_bundle)

    def search(self, ioc_type: str, value: str) -> dict[str, Any]:
        types, normalized = normalize_ioc(ioc_type, value)
        payload = json.dumps({
            "returnFormat": "json", "type": {"OR": types}, "value": normalized,
            "limit": 20, "deleted": 0,
        }).encode("utf-8")
        request = Request(
            f"{self.config.url}/attributes/restSearch", data=payload, method="POST",
            headers={
                "Authorization": self.config.api_key,
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": "open-ng-soc-lab/0.1.0-dev",
            },
        )
        attempts = self.config.max_retries + 1
        for attempt in range(attempts):
            try:
                with self.transport(
                    request,
                    timeout=self.config.connect_timeout + self.config.read_timeout,
                    context=self.context,
                ) as response:
                    raw = response.read(1_048_577)
                    if len(raw) > 1_048_576:
                        raise MispError("MISP response exceeds 1 MiB limit")
                    return self._parse(raw, normalized)
            except HTTPError as exc:
                if exc.code not in RETRYABLE_STATUS or attempt + 1 == attempts:
                    raise MispError(f"MISP HTTP error {exc.code}") from exc
            except (URLError, TimeoutError, socket.timeout) as exc:
                if attempt + 1 == attempts:
                    raise MispError("MISP network timeout or connection failure") from exc
            self.sleeper(0.25 * (2**attempt))
        raise MispError("MISP request failed")

    @staticmethod
    def _parse(raw: bytes, expected_value: str) -> dict[str, Any]:
        try:
            body = json.loads(raw.decode("utf-8"))
            attributes = body.get("response", {}).get("Attribute", [])
        except (UnicodeDecodeError, json.JSONDecodeError, AttributeError) as exc:
            raise MispError("MISP returned invalid JSON") from exc
        if not isinstance(attributes, list):
            raise MispError("MISP response has an invalid Attribute collection")
        matches = []
        for attribute in attributes:
            if not isinstance(attribute, dict) or attribute.get("value") != expected_value:
                continue
            matches.append({
                "type": attribute.get("type"),
                "value": attribute.get("value"),
                "category": attribute.get("category"),
                "to_ids": bool(attribute.get("to_ids", False)),
            })
        return {"misp_match": bool(matches), "match_count": len(matches), "attributes": matches}
