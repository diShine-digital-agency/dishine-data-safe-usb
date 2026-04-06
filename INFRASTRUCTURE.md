# diShine Data-Safe USB - Technical Infrastructure

`Data-Safe USB` is built with a "Privacy-First" (Edge) architecture. It leverages high-performance transformer models to run PII detection locally, avoiding any external data leakage to cloud providers.

---

## 🏗 Technology Stack

- **Data Processing Engine**: [Pandas](https://pandas.pydata.org/)
- **Identification Layer**: [Microsoft Presidio](https://github.com/microsoft/presidio)
- **Natural Language Engine**: [spaCy](https://spacy.io/) (`en_core_web_lg` model)
- **Transformation Layer**: [Faker](https://github.com/joke2k/faker)
- **Language**: Python 3.9+ (Cross-platform)

---

## ⚡ Analysis Architecture: Microsoft Presidio

Standard regex-based anonymizers are prone to missing contextual PII (e.g., names in unstructured cells). `Data-Safe USB` uses Microsoft Presidio, which combines a powerful NLP engine with sophisticated pattern recognition.

### Key Benefits:
- **High Recall**: Detects the widest range of PII (Names, Emails, Locations, IBANs, Credit Cards).
- **Extensible Recognizers**: Can be tuned for specific business data formats.
- **Score-based Detection**: Only flags items with high confidence to minimize over-redaction.

---

## 🔒 Deterministic Transformation Logic

To ensure the resulting AI analysis is contextually accurate (e.g., recognizing that "User A" and "User B" are different entities across rows), we use a **Deterministic Hashing** algorithm with `Faker`.

### Workflow:
1. **Original Value** (e.g., `John Doe`) + **Salt** (diShine-salt) -> **MD5 Hash**.
2. **Hash** is used to seed the `Faker` instance.
3. **Faker** generates a replacement (e.g., `Jane Smith`).
4. Result: The same input siempre gives the same output within the session.

---

## 🏁 Author
**Developed by diShine (Milan, IT)**
*Kevin Escoda*
