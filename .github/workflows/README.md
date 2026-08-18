# Workflow staging

GitHub Actions are intentionally not enabled before a remote exists. Before adding workflows:

- pin every third-party action to a full immutable commit SHA;
- use least-privilege `permissions`;
- avoid exposing secrets to pull requests or untrusted code;
- run XML, JSON/YAML, Markdown, Python, shell, link, and secret checks;
- review Dependabot and security configuration only after the remote exists.
