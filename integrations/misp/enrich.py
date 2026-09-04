#!/usr/bin/env python3
"""Read one synthetic enrichment request from stdin and emit JSON to stdout."""

from __future__ import annotations

import json
import sys

from client import Config, MispClient, MispError


def main() -> int:
    try:
        request = json.load(sys.stdin)
        result = MispClient(Config.from_environment()).search(
            str(request.get("ioc_type", "")), str(request.get("value", ""))
        )
    except (json.JSONDecodeError, AttributeError):
        print(json.dumps({"status": "error", "error": "invalid input JSON"}))
        return 2
    except MispError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}))
        return 1
    print(json.dumps({"status": "ok", **result}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
