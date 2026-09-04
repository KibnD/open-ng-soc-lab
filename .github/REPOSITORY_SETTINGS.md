# Recommended GitHub settings

These settings are prepared for manual review and have not been applied by this branch.

## Metadata

Description: `Reproducible NG-SOC lab with Wazuh, Suricata, MISP, Shuffle and evidence-driven detection tests.`

Topics: `cybersecurity`, `soc`, `ng-soc`, `wazuh`, `suricata`, `misp`, `shuffle`, `threat-intelligence`, `detection-engineering`, `purple-team`, `security-monitoring`, `homelab`, `opensearch`, `incident-response`.

## Main branch ruleset

- Require pull requests and at least one approving review.
- Dismiss stale approvals after new commits.
- Require conversation resolution.
- Require the static-validation checks after their exact GitHub check names are observed.
- Block force pushes and branch deletion.
- Restrict bypass to explicit emergency maintainers and record its use.
- Do not require signed commits until Khalid confirms a workable signing process.

## Security

- Enable Dependabot alerts and security updates.
- Enable secret scanning and push protection if available.
- Enable private vulnerability reporting, then update `SECURITY.md` with the verified channel.
- Enable dependency graph and review CodeQL/Scorecard after the first code-bearing pull request.
- Keep workflow token permissions read-only by default.

Do not enable a required check by guessed name; first push the branch, observe CI, and select the actual successful checks.
