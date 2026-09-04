# Safe MISP lookup adapter

This clean-room adapter searches `POST /attributes/restSearch`, following the [official MISP automation contract](https://github.com/MISP/misp-book/blob/main/automation/README.md). It does not write to the Wazuh queue and is not represented as the private lab script.

Required environment variables are `MISP_URL` and `MISP_API_KEY`. Optional variables are `MISP_CA_BUNDLE`, `MISP_CONNECT_TIMEOUT`, `MISP_READ_TIMEOUT`, and `MISP_MAX_RETRIES`. TLS verification is enabled by default. `MISP_ALLOW_INSECURE_HTTP=1` exists only for an isolated lab and must not be used on untrusted networks.

```sh
printf '%s\n' '{"ioc_type":"ip","value":"198.51.100.42"}' | python integrations/misp/enrich.py
```

The API key is placed only in the authorization header and never printed. Responses are capped at 1 MiB. Retries are bounded and limited to connection errors, timeouts, HTTP 429, 502, 503, and 504. On failure, callers retain the original alert and treat enrichment as unavailable—not as a match.

Tests use synthetic responses and make no network connection. This component remains pre-release until its Python tests run successfully and it is exercised against an authorized MISP instance.
