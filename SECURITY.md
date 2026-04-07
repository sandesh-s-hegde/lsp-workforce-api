# 🛡️ Security Policy

We take the security of B2B fleet telemetry, partner credentials, and downstream logistics execution with the utmost seriousness. This document outlines our security support lifecycle and Coordinated Vulnerability Disclosure (CVD) process.

## 📦 Supported Versions

Security updates and critical patches are actively provided for the following release branches:

| Version | Status | Support Level |
| :--- | :--- | :--- |
| **1.0.x** | :white_check_mark: Active | Full Security & Bug Fix Support |
| **< 1.0** | :x: Deprecated | Unsupported (Upgrade required) |

*Note: As this API acts as the execution middleware within a broader Tripartite Ecosystem, we strongly recommend that consumers strictly pin their dependencies to the latest `1.0.x` stable tag.*

## 🎯 Threat Scope

When auditing this repository, the following vectors are considered **In-Scope** for critical security patches:
* **Authentication & Authorization:** Bypasses to the API Key validation middleware or cross-tenant data leakage (e.g., Partner A reading Partner B's bookings).
* **Data Persistence:** SQL Injection (SQLi) vulnerabilities bypassing the SQLAlchemy ORM layer.
* **Denial of Service (DoS):** Application-layer bottlenecks that bypass the `slowapi` rate-limiting configurations.
* **Ecosystem Lateral Movement:** Vulnerabilities that allow malicious payloads to be passed upstream to the Digital Capacity Twin or downstream to the RPA Legacy Freight Bridge.

**Out of Scope:**
* Volumetric Network DDoS attacks (mitigated at the cloud infrastructure layer, not the application layer).
* Vulnerabilities originating from third-party fleet supplier APIs (e.g., Enterprise, Ryder).

## 🚨 Reporting a Vulnerability

**Please do NOT create a public GitHub issue for security vulnerabilities.** Public disclosure before a patch is available puts our production environments and integration partners at risk. We practice Coordinated Vulnerability Disclosure.

1. **Report:** Email the repository maintainer directly with the subject line: `[SECURITY] Vulnerability Report - B2B Fleet Aggregator`.
2. **Include:** Provide a clear description of the vulnerability, the exact endpoint(s) affected, and steps to reproduce (or a Proof of Concept script). 
3. **Triage SLA:** We will acknowledge receipt of your vulnerability report within **48 hours**.
4. **Remediation SLA:** Verified vulnerabilities will be patched in a private fork, merged, and released as a hotfix (`v1.0.x+1`) within **7 to 14 days**, depending on severity.
5. **Disclosure:** Once the patch is deployed and downstream consumers are notified, we will publicly acknowledge your contribution in our Release Notes (unless you request to remain anonymous).