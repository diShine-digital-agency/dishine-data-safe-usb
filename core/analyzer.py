from presidio_analyzer import AnalyzerEngine
import os

class PII_Analyzer:
    def __init__(self, model="en_core_web_lg"):
        self.analyzer = AnalyzerEngine(default_score_threshold=0.4)
        self.entities = [
            "PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER", "LOCATION", 
            "IBAN_CODE", "CREDIT_CARD", "CRYPTO", "DATE_TIME"
        ]

    def analyze_text(self, text):
        if not isinstance(text, str) or not text.strip():
            return []
        
        results = self.analyzer.analyze(
            text=text,
            entities=self.entities,
            language='en'
        )
        return results

if __name__ == "__main__":
    # Test
    analyzer = PII_Analyzer()
    test_text = "Alice Smith (alice@example.com) discussed her IBAN DE89 3704 0044 0532 01"
    res = analyzer.analyze_text(test_text)
    for r in res:
        print(f"Found: {r.entity_type} at {r.start}-{r.end} (Score: {r.score:.2f})")
