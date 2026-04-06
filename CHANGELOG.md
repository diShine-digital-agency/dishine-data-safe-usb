# Changelog

All notable changes to this project will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2026-04-06

### Added
- Batch processing: all CSV files in the input directory are now processed in a single run.
- `--dry-run` flag to preview PII detection without modifying files.
- `--input` and `--output` CLI arguments for custom directories.
- Summary report table after processing, showing per-file replacement counts and detected PII types.
- Configurable salt via `DATASAFE_SALT` environment variable.
- Test suite with 15 tests covering transformer, vault, and full pipeline.
- `.gitkeep` files for `output/` and `vault/` directories.
- `DATE_TIME` and `CRYPTO` entity type handling in the transformer.

### Changed
- Lowered PII detection confidence threshold from 0.4 to 0.3 for better recall on phone numbers and IBANs.
- Switched deterministic hashing from MD5 to SHA-256.
- Replaced `iterrows()` with index-based iteration for better performance.
- Updated `requirements.txt` to use compatible version ranges instead of pinned versions.
- Improved `setup.sh` with error handling, idempotent venv creation, and requirements.txt-based installs.
- Rewrote README, GUIDE, and INFRASTRUCTURE documentation for accuracy and clarity.

### Fixed
- `core/__init__.py` syntax error (bare text instead of comment).
- Detection results now sorted by confidence score so the best match is used for replacement.
- CSV loading now handles encoding issues with UTF-8/Latin-1 fallback.
- Empty CSV files and `nan` values are now handled gracefully.

### Security
- Added `vault/`, `output/`, `venv/`, `__pycache__/` to `.gitignore`.
- Removed previously committed output data and vault mapping from git tracking.
- Removed inaccurate "encrypted vault" claim from documentation.

---

## [1.0.0] - 2026-04-06

### Added
- Core PII detection engine using Microsoft Presidio.
- Deterministic fake data generation with Faker.
- Local vault for storing original-to-fake mappings as JSON.
- macOS `.command` launcher and `setup.sh` for environment setup.
- CSV processing with pandas.
- Documentation: README, GUIDE, INFRASTRUCTURE, CHANGELOG.

---

Author: Kevin Escoda · [diShine](https://dishine.it)
