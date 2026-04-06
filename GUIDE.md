# Data-Safe USB - Operational Guide 🧭

This guide provides step-by-step instructions for HR, Ops, and Compliance teams to safely prepare sensitive CSV data for analysis in the cloud.

---

## Technical Prerequisites

To use `Data-Safe USB`, your Mac must have **Python 3.9+** and **Pip** installed. The provided `setup.sh` script will handle the rest.

---

## 🧭 Workflow Walkthrough

### 1. Preparation (One-time only)
Run the setup script while connected to the internet to download the PII detection models and Python libraries.
```bash
./setup.sh
```

### 2. High-Confidentiality Sessions
For maximum security, you can **disconnect your internet connection** after setup. The transcription and anonymization engine will run entirely offline.

### 3. Anonymizing Your CSV
1. **Source**: Ensure your CSV file has a header row (e.g., `Name`, `Email`, `Phone`).
2. **Input**: Copy your raw data into the `input/` folder.
3. **Execute**: Launch the app by double-clicking `Data_Safe.command`.
4. **Anonymization**: The system will scan every cell. PII will be replaced by deterministic fake data (e.g., `John Doe` -> `Jane Smith`).
5. **Output**: Your safe-to-upload file will be in the `output/` folder, prefixed with `safe_`.
6. **The Vault**: A dictionary mapping real PII to fake data is saved in the `/vault` folder. **Never share this folder.**

---

## ❓ Frequently Asked Questions

- **"No CSV files found"**: Ensure your file is in the `input/` folder and has a `.csv` extension.
- **"Why is it taking long?"**: Deep NLP analysis of large datasets (10k+ rows) can take several minutes on older CPUs. 
- **"Is it REALLY safe?"**: Yes. The `analyzer` uses Microsoft Presidio, a highly accurate PII detection engine. However, we always recommend a quick manual spot-check of the `output/` file for any edge-case formatting.

---

## 🏁 Author
**Developed by diShine (Milan, IT)**
*Kevin Escoda*
