# Data-Safe USB — Technical Infrastructure

This document describes the architecture, dependencies, and design decisions behind Data-Safe USB.

---

## Technology Stack

| Component | Library | Purpose |
|-----------|---------|---------|
| Data Processing | [pandas](https://pandas.pydata.org/) | CSV reading, manipulation, and writing |
| PII Detection | [Microsoft Presidio](https://github.com/microsoft/presidio) | NLP-based entity recognition |
| NLP Engine | [spaCy](https://spacy.io/) (`en_core_web_lg`) | Language model for text analysis |
| Fake Data | [Faker](https://github.com/joke2k/faker) | Deterministic replacement generation |
| CLI Interface | [Rich](https://github.com/Textualize/rich) | Progress bars, tables, formatted output |
| Language | Python 3.9+ | Cross-platform |

---

## PII Detection

Standard regex-based anonymizers miss contextual PII — a name in an unstructured cell, or a location mentioned informally. Data-Safe USB uses Microsoft Presidio, which combines spaCy's NLP pipeline with pattern recognizers and contextual scoring.

**Supported entity types:**
- `PERSON` — full names
- `EMAIL_ADDRESS` — email addresses
- `PHONE_NUMBER` — phone numbers in various formats
- `LOCATION` — street addresses, cities, countries
- `IBAN_CODE` — international bank account numbers
- `CREDIT_CARD` — credit card numbers
- `DATE_TIME` — dates and timestamps
- `CRYPTO` — cryptocurrency wallet addresses

**Detection threshold:** The analyzer uses a confidence score threshold of 0.3 (configurable). Only values that Presidio identifies with sufficient confidence are flagged for replacement. This balances recall against over-redaction.

---

## Deterministic Transformation

To preserve data relationships (so downstream AI analysis can still distinguish between "User A" and "User B" across rows), replacements are deterministic rather than random.

**How it works:**

1. Take the original value (e.g., `John Doe`) and a salt string.
2. Compute `SHA-256(salt + ":" + original_value)`.
3. Use the resulting hash as a seed for the Faker library.
4. Faker generates a type-appropriate replacement (e.g., a fake name for a `PERSON`, a fake email for an `EMAIL_ADDRESS`).

The same input always produces the same output within a session. Different salts produce different outputs, which provides a basic layer of protection if the algorithm is known.

The salt defaults to `diShine-salt` but can be overridden via the `DATASAFE_SALT` environment variable.

---

## Vault Storage

After processing, the tool saves a JSON file (`vault/mapping_key.json`) containing every original → fake pair. This serves as the reversal key.

The vault is stored as **plain-text JSON**. It is not encrypted at the application level. For environments that require encryption at rest, use OS-level disk encryption (FileVault on macOS, LUKS on Linux, BitLocker on Windows).

The `vault/` directory is excluded from git via `.gitignore` to prevent accidental commits.

---

## Processing Pipeline

```
1. Load CSV(s) from input/ directory
2. For each row and each cell:
   a. Run Presidio analyzer → get list of detected PII entities
   b. Pick the highest-confidence entity type
   c. Generate a deterministic fake via SHA-256-seeded Faker
   d. Replace the cell value
3. Write anonymized CSV to output/ with "safe_" prefix
4. Save the complete mapping to vault/mapping_key.json
```

---

## Limitations

- **Single-entity cells:** The current implementation assumes each cell contains one primary PII type. Cells with mixed PII (e.g., "John Doe (john@example.com)") will be replaced based on the highest-confidence entity only.
- **Language support:** The spaCy model is English-only (`en_core_web_lg`). Non-English PII may not be detected.
- **Memory:** All data is loaded into memory via pandas. Very large files (1 GB+) may require sufficient RAM.
- **Detection accuracy:** No PII detector is perfect. Always spot-check the output for edge cases.

---

Copyright © 2026 [diShine](https://dishine.it). All rights reserved.
Author: Kevin Escoda
