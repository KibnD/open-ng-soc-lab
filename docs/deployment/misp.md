# MISP deployment

MISP is a private-lab CTI service reached over HTTPS/443. Install it using supported upstream guidance and isolate administrative access.

## Integration requirements

- Store the URL and API key in environment variables or a secret store.
- Verify TLS by default; optionally provide a private CA path.
- Configure connection and read timeouts.
- Use bounded retries only for safe/idempotent requests.
- Validate IOC types and normalize values before queries.
- Fail closed for enrichment: preserve the original Wazuh alert and record an enrichment error without inventing a match.
- Cache safe negative results briefly where appropriate to avoid unnecessary CTI requests.

Do not import or redistribute third-party feeds without confirming their licenses. Use synthetic IOCs such as RFC 5737 addresses for public tests.

Health checks must avoid displaying API keys. Confirm HTTPS, authenticated API behavior, database/container health, and free disk space. Back up MISP configuration/database privately; revoke test keys during cleanup.
