from presidio_analyzer import AnalyzerEngine


class PII_Analyzer:
    """Detects PII entities in text using Microsoft Presidio."""

    DEFAULT_ENTITIES = [
        "PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER", "LOCATION",
        "IBAN_CODE", "CREDIT_CARD", "CRYPTO", "DATE_TIME",
        "IP_ADDRESS", "URL",
    ]

    def __init__(self, score_threshold=0.3, entities=None):
        self.analyzer = AnalyzerEngine()
        self.score_threshold = score_threshold
        self.entities = entities or self.DEFAULT_ENTITIES

    def analyze_text(self, text):
        """Return a list of PII recognition results for the given text."""
        if not isinstance(text, str) or not text.strip():
            return []

        results = self.analyzer.analyze(
            text=text,
            entities=self.entities,
            language="en",
            score_threshold=self.score_threshold,
        )
        # Sort by confidence score descending
        results.sort(key=lambda r: r.score, reverse=True)
        return results


if __name__ == "__main__":
    analyzer = PII_Analyzer()
    test_text = "Alice Smith (alice@example.com) discussed her IBAN DE89 3704 0044 0532 01"
    res = analyzer.analyze_text(test_text)
    for r in res:
        print(f"Found: {r.entity_type} at {r.start}-{r.end} (Score: {r.score:.2f})")
