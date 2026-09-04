# Trust boundaries

Treat endpoints, network telemetry, the detection core, CTI/SOAR, and external notification as separate trust zones. Authenticate every cross-zone service, restrict allowed sources, and prefer encrypted transport.

The private laboratory accepts two intentional risks that must not be copied into production: UDP Syslog and HTTP delivery from Wazuh to Shuffle. This repository does not claim compensating controls sufficient for production use.

Secrets belong in runtime secret stores or environment variables, never source files, workflow exports, screenshots, fixtures, logs, or GitHub Actions output.
