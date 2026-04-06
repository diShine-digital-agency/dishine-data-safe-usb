import os
import json
import tempfile

import pytest

from core.transformer import PII_Transformer
from core.vault import DataVault


class TestPIITransformer:
    """Tests for the PII_Transformer class."""

    def test_deterministic_output(self):
        """Same input should always produce the same fake value."""
        t = PII_Transformer(salt="test-salt")
        result1 = t.get_deterministic_fake("John Doe", "PERSON")
        result2 = t.get_deterministic_fake("John Doe", "PERSON")
        assert result1 == result2

    def test_different_inputs_produce_different_outputs(self):
        """Different original values should produce different fakes."""
        t = PII_Transformer(salt="test-salt")
        fake_a = t.get_deterministic_fake("John Doe", "PERSON")
        fake_b = t.get_deterministic_fake("Jane Smith", "PERSON")
        assert fake_a != fake_b

    def test_mapping_is_recorded(self):
        """Every replacement should be recorded in the mapping dict."""
        t = PII_Transformer(salt="test-salt")
        t.get_deterministic_fake("alice@example.com", "EMAIL_ADDRESS")
        assert "alice@example.com" in t.mapping

    def test_supported_entity_types(self):
        """All supported entity types should produce a non-empty string."""
        t = PII_Transformer(salt="test-salt")
        for entity_type in PII_Transformer.ENTITY_GENERATORS:
            result = t.get_deterministic_fake(f"test-{entity_type}", entity_type)
            assert result, f"Empty result for {entity_type}"
            assert "[REDACTED" not in result

    def test_unknown_entity_type_redacted(self):
        """Unknown entity types should be replaced with a REDACTED tag."""
        t = PII_Transformer(salt="test-salt")
        result = t.get_deterministic_fake("mystery", "UNKNOWN_TYPE")
        assert result == "[REDACTED_UNKNOWN_TYPE]"

    def test_custom_salt(self):
        """Different salts should produce different outputs for the same input."""
        t1 = PII_Transformer(salt="salt-one")
        t2 = PII_Transformer(salt="salt-two")
        fake1 = t1.get_deterministic_fake("John Doe", "PERSON")
        fake2 = t2.get_deterministic_fake("John Doe", "PERSON")
        assert fake1 != fake2

    def test_salt_from_env(self, monkeypatch):
        """Salt should be read from DATASAFE_SALT env variable when not provided."""
        monkeypatch.setenv("DATASAFE_SALT", "env-salt")
        t = PII_Transformer()
        assert t.salt == "env-salt"


class TestDataVault:
    """Tests for the DataVault class."""

    def test_save_and_load_mapping(self):
        """Saving a mapping and loading it back should return identical data."""
        with tempfile.TemporaryDirectory() as tmpdir:
            vault = DataVault(vault_dir=tmpdir)
            mapping = {"John Doe": "Fake Name", "alice@test.com": "fake@test.com"}
            vault.save_mapping(mapping)
            loaded = vault.load_mapping()
            assert loaded == mapping

    def test_load_missing_mapping_returns_empty(self):
        """Loading from a non-existent file should return an empty dict."""
        with tempfile.TemporaryDirectory() as tmpdir:
            vault = DataVault(vault_dir=tmpdir)
            result = vault.load_mapping("nonexistent.json")
            assert result == {}

    def test_save_creates_file(self):
        """Saving should create the JSON file on disk."""
        with tempfile.TemporaryDirectory() as tmpdir:
            vault = DataVault(vault_dir=tmpdir)
            vault.save_mapping({"key": "value"})
            assert os.path.isfile(os.path.join(tmpdir, "mapping_key.json"))

    def test_vault_creates_directory(self):
        """DataVault should create its directory if it doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            vault_path = os.path.join(tmpdir, "new_vault")
            vault = DataVault(vault_dir=vault_path)
            assert os.path.isdir(vault_path)

    def test_unicode_mapping(self):
        """Mappings with unicode characters should be preserved."""
        with tempfile.TemporaryDirectory() as tmpdir:
            vault = DataVault(vault_dir=tmpdir)
            mapping = {"José García": "Fake José", "田中太郎": "Fake 太郎"}
            vault.save_mapping(mapping)
            loaded = vault.load_mapping()
            assert loaded == mapping


class TestIntegration:
    """Integration tests for the full pipeline."""

    def test_csv_processing_pipeline(self):
        """Full pipeline: CSV in → anonymized CSV out + vault mapping."""
        import pandas as pd

        with tempfile.TemporaryDirectory() as tmpdir:
            input_dir = os.path.join(tmpdir, "input")
            output_dir = os.path.join(tmpdir, "output")
            os.makedirs(input_dir)
            os.makedirs(output_dir)

            # Create test CSV
            test_csv = os.path.join(input_dir, "test.csv")
            df = pd.DataFrame({
                "Name": ["John Doe", "Jane Smith"],
                "Email": ["john@example.com", "jane@example.com"],
            })
            df.to_csv(test_csv, index=False)

            # Import and run processor
            from Data_Safe import process_csv
            from core.analyzer import PII_Analyzer
            from core.transformer import PII_Transformer

            analyzer = PII_Analyzer()
            transformer = PII_Transformer(salt="test")
            result = process_csv(test_csv, output_dir, analyzer, transformer)

            assert result is not None
            assert result["rows"] == 2
            assert result["replacements"] > 0

            # Check output file exists
            output_file = os.path.join(output_dir, "safe_test.csv")
            assert os.path.isfile(output_file)

            # Check output differs from input
            output_df = pd.read_csv(output_file)
            assert not output_df.equals(df)

    def test_dry_run_does_not_modify(self):
        """Dry-run mode should not write output files."""
        import pandas as pd

        with tempfile.TemporaryDirectory() as tmpdir:
            input_dir = os.path.join(tmpdir, "input")
            output_dir = os.path.join(tmpdir, "output")
            os.makedirs(input_dir)
            os.makedirs(output_dir)

            test_csv = os.path.join(input_dir, "test.csv")
            df = pd.DataFrame({"Name": ["Alice Johnson"]})
            df.to_csv(test_csv, index=False)

            from Data_Safe import process_csv
            from core.analyzer import PII_Analyzer
            from core.transformer import PII_Transformer

            analyzer = PII_Analyzer()
            transformer = PII_Transformer(salt="test")
            result = process_csv(test_csv, output_dir, analyzer, transformer, dry_run=True)

            output_file = os.path.join(output_dir, "safe_test.csv")
            assert not os.path.isfile(output_file)

    def test_empty_csv_skipped(self):
        """Empty CSV files should be skipped gracefully."""
        import pandas as pd

        with tempfile.TemporaryDirectory() as tmpdir:
            input_dir = os.path.join(tmpdir, "input")
            output_dir = os.path.join(tmpdir, "output")
            os.makedirs(input_dir)
            os.makedirs(output_dir)

            test_csv = os.path.join(input_dir, "empty.csv")
            pd.DataFrame().to_csv(test_csv, index=False)

            from Data_Safe import process_csv
            from core.analyzer import PII_Analyzer
            from core.transformer import PII_Transformer

            analyzer = PII_Analyzer()
            transformer = PII_Transformer(salt="test")
            result = process_csv(test_csv, output_dir, analyzer, transformer)
            assert result is None
