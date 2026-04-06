# diShine Data-Safe USB (v1.0.0)

**100% GDPR-Compliant Local Anonymizer for Secure AI Analysis.**

Modern businesses want the power of LLMs (ChatGPT, Claude) for data analysis, but uploading raw customer lists, HR records, or sales data is a massive compliance risk. `Data-Safe USB` is a local-first Python engine that scrubs PII (Personally Identifiable Information) from your CSVs before they ever reach the cloud.

Built by [diShine](https://dishine.it)

---

## The Business Logic

Cloud AI is transformative, but **Privacy is Non-Negotiable.** 

`Data-Safe USB` provides a "pre-processing" layer that ensures no real names, emails, phone numbers, or IBANs are uploaded to external servers. By replacing sensitive data with realistic, deterministic fake data, your AI models can still perform meaningful analysis (e.g., trend detection, grouping) without violating GDPR or internal security policies.

---

## Features

- **Local Discovery**: Powered by Microsoft Presidio and spaCy for deep NLP-based PII detection.
- **Realistic Transformation**: Uses the `Faker` library to generate consistent, deterministic replacements (e.g., "John Doe" becomes "Jane Smith").
- **Deterministic Mapping**: Maintains consistency across files; the same original value will always receive the same fake value within a session.
- **Local Vault**: Stores the "Original -> Fake" mapping key locally in an encrypted vault, allowing you to reverse the process if needed.
- **Mac-Native Experience**: One-click `.command` launcher for non-technical Ops/HR teams.

---

## Quick Start

1. **Setup**: Run `setup.sh` to initialize the environment.
   ```bash
   ./setup.sh
   ```
2. **Deposit Data**: Drop your raw CSV into the `input/` folder.
3. **Execute**: Run `Data_Safe.command`.
4. **Result**: Your scrubbed, safe-to-upload file appears in `output/`.

---

## Security Architecture

1. **In-Memory Analysis**: Data is processed in local RAM. No data is stored or logged.
2. **PII Detection**: Multi-layer scanner (Regex + Transformer models) identifies names, emails, phones, and financial identifiers.
3. **Vault Isolation**: The mapping key is kept in the `/vault` directory, which should never be uploaded.

---

## About diShine

[diShine](https://dishine.it) is a Milan-based creative tech agency. We build tools for digital consultants, help businesses with AI strategy and MarTech architecture, and bridge the gap between "Edge Intelligence" and "Cloud Power."

- Web: [dishine.it](https://dishine.it)
- GitHub: [github.com/diShine-digital-agency](https://github.com/diShine-digital-agency)

Copyright (c) 2026 [diShine](https://dishine.it). All rights reserved.
**Author: Kevin Escoda**
