# Shuffle deployment

In the confirmed lab, Shuffle's frontend/reverse-proxy endpoint is HTTP/3001 and its backend port 5001 is internal. HTTPS/3443 applies only when separately configured; these ports are not universal deployment guarantees.

## Safe workflow contract

The planned public template accepts a minimal Wazuh alert, performs a MISP lookup, branches on `misp_match=true`, handles no-match and error paths, and sends a generic notification. Webhook IDs, authentication objects, Slack channel IDs, tokens, execution history, and private names must be absent.

Use HTTPS outside an isolated lab. Configure URLs, credentials, CA trust, destination, and timeouts as runtime variables or secrets. Limit webhook sources and validate payload shape before processing.

Verify frontend/API reachability, backend and worker health, all Swarm services at expected replicas, and a synthetic match/no-match/error sequence. Cleanup deletes the disposable webhook and test authentication objects and confirms they no longer work.
