# Shuffle workflow blueprint

`workflow-blueprint.json` is a sanitized, product-neutral build contract. It is deliberately **not claimed to be a directly importable Shuffle export**: current exports contain node UUIDs, app-version references, organization data, and authentication references that must be generated or selected inside the target Shuffle instance.

## Manual build

1. Create a new private workflow; do not duplicate the operational lab workflow.
2. Add a generic Webhook trigger and restrict its callers.
3. Validate the input against [`wazuh-alert.schema.json`](wazuh-alert.schema.json).
4. Extract `data.srcip` only after validation.
5. Call the MISP adapter or `POST /attributes/restSearch` over verified HTTPS.
6. Add an explicit condition for `misp_match == true`.
7. Route `true` to the generic Slack notification, `false` to a no-match result, and network/JSON failures to an unavailable result.
8. Configure secrets in Shuffle authentication/KMS facilities, never workflow variables or exported JSON.
9. Test the match, no-match, malformed-payload, timeout, and server-error cases.
10. Export the new workflow, run the publication validator, inspect every field manually, then import it into a disposable Shuffle instance before calling it portable.

Shuffle's official documentation warns that exports include authentication references. The publication-ready export therefore remains `target` until the lab-generated candidate is sanitized and import-tested.

## Ports

The private lab uses frontend/reverse proxy HTTP/3001 and internal backend 5001. HTTPS/3443 applies only if configured. These are not universal Shuffle backend ports.
