from faker import Faker
import hashlib

class PII_Transformer:
    def __init__(self, seed="diShine-salt"):
        self.faker = Faker()
        self.salt = seed
        self.mapping = {}

    def get_deterministic_fake(self, original_value, entity_type):
        """
        Generates a consistent fake value for a given original value.
        """
        if original_value in self.mapping:
            return self.mapping[original_value]
            
        # Seed Faker with original value to be deterministic per value
        # This allows CSV joining by maintaining consistency
        combined = f"{self.salt}:{original_value}"
        hash_val = int(hashlib.md5(combined.encode()).hexdigest(), 16)
        self.faker.seed_instance(hash_val)
        
        fake_val = ""
        if entity_type == "PERSON":
            fake_val = self.faker.name()
        elif entity_type == "EMAIL_ADDRESS":
            fake_val = self.faker.email()
        elif entity_type == "PHONE_NUMBER":
            fake_val = self.faker.phone_number()
        elif entity_type == "LOCATION":
            fake_val = self.faker.address()
        elif entity_type == "IBAN_CODE":
            fake_val = self.faker.iban()
        elif entity_type == "CREDIT_CARD":
            fake_val = self.faker.credit_card_number()
        else:
            fake_val = f"[REDACTED_{entity_type}]"
            
        self.mapping[original_value] = fake_val
        return fake_val

if __name__ == "__main__":
    # Test
    transformer = PII_Transformer()
    print(f"Original: John Doe -> {transformer.get_deterministic_fake('John Doe', 'PERSON')}")
    print(f"Original: John Doe -> {transformer.get_deterministic_fake('John Doe', 'PERSON')} (Should match)")
    print(f"Original: Jane Doe -> {transformer.get_deterministic_fake('Jane Doe', 'PERSON')}")
