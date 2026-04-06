# Changelog - diShine Data-Safe USB

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-04-06

### Added
- **Core Engine**: Implementation of Microsoft Presidio for local PII analysis.
- **Transformation Layer**: Deterministic `Faker` generator for realistic data replacement.
- **Vault Mapping**: Local JSON-based mapping storage for reversing anonymization.
- **Mac Launchers**: Double-clickable `.command` file and automated `setup.sh`.
- **Documentation Suite**: High-impact README, operational GUIDE, and technical INFRASTRUCTURE docs.
- **CSV Support**: Full integration with `pandas` for processing tabular datasets.

### Changed
- Refined PII detection threshold for safer, high-confidence redaction.

### Fixed
- Deterministic seeding to ensure consistent replacements within a session.

---

## 🏁 Author
**Developed by diShine (Milan, IT)**
*Kevin Escoda*
