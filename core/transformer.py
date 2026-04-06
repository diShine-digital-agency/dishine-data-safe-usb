import hashlib
import os

from faker import Faker


class PII_Transformer:
    """Generates deterministic fake values to replace detected PII."""

    ENTITY_GENERATORS = {
        "PERSON": "name",
        "EMAIL_ADDRESS": "email",
        "PHONE_NUMBER": "phone_number",
        "LOCATION": "address",
        "IBAN_CODE": "iban",
        "CREDIT_CARD": "credit_card_number",
        "DATE_TIME": "date",
        "CRYPTO": "sha1",
    }

    def __init__(self, salt=None):
        self.faker = Faker()
        self.salt = salt or os.environ.get("DATASAFE_SALT", "diShine-salt")
        self.mapping = {}

    def get_deterministic_fake(self, original_value, entity_type):
        """Return a consistent fake value for the given original value."""
        if original_value in self.mapping:
            return self.mapping[original_value]

        # Seed Faker deterministically so the same input always produces the same output
        combined = f"{self.salt}:{original_value}"
        hash_val = int(hashlib.sha256(combined.encode()).hexdigest(), 16)
        self.faker.seed_instance(hash_val)

        generator_name = self.ENTITY_GENERATORS.get(entity_type)
        if generator_name:
            fake_val = getattr(self.faker, generator_name)()
        else:
            fake_val = f"[REDACTED_{entity_type}]"

        self.mapping[original_value] = fake_val
        return fake_val


if __name__ == "__main__":
    transformer = PII_Transformer()
    print(f"Original: John Doe -> {transformer.get_deterministic_fake('John Doe', 'PERSON')}")
    print(f"Original: John Doe -> {transformer.get_deterministic_fake('John Doe', 'PERSON')} (Should match)")
    print(f"Original: Jane Doe -> {transformer.get_deterministic_fake('Jane Doe', 'PERSON')}")
