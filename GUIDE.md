# Data-Safe USB — Operational Guide

Step-by-step instructions for preparing sensitive CSV data for cloud analysis.

---

## Prerequisites

- **Python 3.9+** installed on your machine
- **Internet connection** for the initial setup (to download NLP models)
- A CSV file with a header row (e.g., `Name`, `Email`, `Phone`)

---

## Initial Setup (One-Time)

Run the setup script to create a virtual environment and download the required models:

```bash
chmod +x setup.sh
./setup.sh
```

This takes a few minutes depending on your internet speed. The spaCy language model is about 400 MB.

If setup fails partway through, delete the `venv/` folder and run the script again.

---

## Anonymizing Your Data

### Step 1: Place your CSV file(s)

Copy your raw CSV file(s) into the `input/` folder. Each file should have a header row with column names.

### Step 2: Run the tool

**On macOS:** Double-click `Data_Safe.command`.

**On any platform:**
```bash
source venv/bin/activate
python Data_Safe.py
```

### Step 3: Collect the output

Your anonymized file(s) will appear in the `output/` folder, prefixed with `safe_`. For example, `clients.csv` becomes `safe_clients.csv`.

### Step 4: Verify

Open the output file and spot-check a few rows to confirm that PII has been replaced. You can also run:

```bash
python Data_Safe.py --dry-run
```

This scans for PII and shows you what would be replaced without actually modifying any files.

---

## Working Offline

After the initial setup, the tool runs entirely offline. For maximum security during sensitive sessions, you can disconnect from the internet before processing your data. No data is ever sent to an external server.

---

## The Vault

After processing, a file called `mapping_key.json` is saved in the `vault/` folder. This file contains the mapping between original values and their fake replacements.

**Important:** This file is the reversal key. If someone has it, they can undo the anonymization. Keep it secure and never share it or upload it to any cloud service.

---

## Processing Multiple Files

The tool processes all CSV files in the `input/` directory in a single run. Each file gets its own output file in `output/`.

---

## Troubleshooting

**"No CSV files found"**
Make sure your file is in the `input/` folder and has a `.csv` extension.

**Processing is slow**
NLP-based analysis of large datasets (10,000+ rows) can take several minutes. This is expected behavior — the tool is analyzing every cell individually.

**Encoding errors**
The tool tries UTF-8 first, then falls back to Latin-1 encoding. If your CSV uses a different encoding, convert it to UTF-8 before processing.

**Some values were not replaced**
The PII detector uses confidence scoring. Values that don't clearly look like personal data (short abbreviations, ambiguous strings) may not be flagged. Always do a manual spot-check of the output.

---

Copyright © 2026 [diShine](https://dishine.it). All rights reserved.
Author: Kevin Escoda
