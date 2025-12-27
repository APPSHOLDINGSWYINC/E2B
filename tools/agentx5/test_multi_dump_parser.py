"""
Test suite for multi_dump_parser.py

Tests the parsing, section detection, and output generation
for various data formats.
"""
import pytest
import tempfile
import shutil
from pathlib import Path
import pandas as pd
import json
import sys
import os

# Add parent directory to path to import multi_dump_parser
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from multi_dump_parser import (
    parse_file,
    write_sections,
    compute_capital_gains,
    HEADER_PATTERNS,
    JSON_SECTIONS,
)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test outputs."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    # Cleanup after tests
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_robinhood_data():
    """Sample Robinhood sales data."""
    return """ASSET NAME,RECEIVED DATE,COST BASIS(USD),DATE SOLD,PROCEEDS
AAPL,2020-01-01,100.00,2021-01-01,150.00
TSLA,2020-06-01,200.00,2020-12-01,250.00
GOOGL,2019-01-01,1000.00,2021-06-01,1500.00"""


@pytest.fixture
def sample_crypto_data():
    """Sample crypto movements data."""
    return """Transaction,Type,Input Currency,Input Amount,Output Currency
TX001,Buy,USD,1000.00,BTC
TX002,Sell,BTC,0.5,USD
TX003,Transfer,ETH,2.0,ETH"""


@pytest.fixture
def sample_btc_prices():
    """Sample BTC daily prices."""
    return """Start,End,Open,High,Low,Close,Volume,Market Cap
2021-01-01,2021-01-02,30000,31000,29000,30500,1000000,500000000
2021-01-02,2021-01-03,30500,32000,30000,31500,1200000,520000000"""


@pytest.fixture
def sample_json_data():
    """Sample Logic App JSON data."""
    return '{"$schema": "https://schema.management.azure.com/", "contentVersion": "1.0.0.0"}'


@pytest.fixture
def sample_scriptable_js():
    """Sample Scriptable JS code."""
    return """// Variables used by Scriptable.
// These must be at the very top of the file. Do not edit.
let widget = new Widget();
widget.addText("Hello World");"""


class TestHeaderPatterns:
    """Test header pattern recognition."""

    def test_robinhood_pattern_matches(self):
        header = "ASSET NAME,RECEIVED DATE,COST BASIS(USD),DATE SOLD,PROCEEDS"
        assert HEADER_PATTERNS["robinhood_sales"].search(header) is not None

    def test_crypto_pattern_matches(self):
        header = "Transaction,Type,Input Currency,Input Amount,Output Currency"
        assert HEADER_PATTERNS["crypto_movements"].search(header) is not None

    def test_btc_pattern_matches(self):
        header = "Start,End,Open,High,Low,Close,Volume,Market Cap"
        assert HEADER_PATTERNS["btc_daily_prices"].search(header) is not None

    def test_personal_finance_pattern_matches(self):
        header = "Date,Original Date,Account Type,Account Name,Account Number,Institution Name"
        assert HEADER_PATTERNS["personal_finance"].search(header) is not None


class TestParseFile:
    """Test file parsing functionality."""

    def test_parse_robinhood_section(self, temp_dir, sample_robinhood_data):
        input_file = temp_dir / "test_input.txt"
        input_file.write_text(sample_robinhood_data)

        sections = parse_file(input_file)

        assert "robinhood_sales" in sections
        assert len(sections["robinhood_sales"]) == 4  # header + 3 data rows

    def test_parse_multiple_sections(
        self, temp_dir, sample_robinhood_data, sample_crypto_data
    ):
        combined_data = f"{sample_robinhood_data}\n\n{sample_crypto_data}"
        input_file = temp_dir / "test_input.txt"
        input_file.write_text(combined_data)

        sections = parse_file(input_file)

        assert "robinhood_sales" in sections
        assert "crypto_movements" in sections
        assert len(sections) == 2

    def test_parse_json_section(self, temp_dir, sample_json_data):
        input_file = temp_dir / "test_input.txt"
        input_file.write_text(sample_json_data)

        sections = parse_file(input_file)

        assert "logic_app_json" in sections
        assert sections["logic_app_json"][0].startswith('{"$schema"')

    def test_parse_scriptable_js(self, temp_dir, sample_scriptable_js):
        input_file = temp_dir / "test_input.txt"
        input_file.write_text(sample_scriptable_js)

        sections = parse_file(input_file)

        assert "scriptable_js" in sections
        assert "Variables used by Scriptable" in sections["scriptable_js"][0]

    def test_parse_empty_file(self, temp_dir):
        input_file = temp_dir / "test_input.txt"
        input_file.write_text("")

        sections = parse_file(input_file)

        assert sections == {}


class TestWriteSections:
    """Test section writing functionality."""

    def test_write_csv_section(self, temp_dir, sample_robinhood_data):
        input_file = temp_dir / "test_input.txt"
        input_file.write_text(sample_robinhood_data)

        sections = parse_file(input_file)
        output_dir = temp_dir / "output"
        write_sections(sections, output_dir)

        output_file = output_dir / "robinhood_sales.csv"
        assert output_file.exists()

        # Verify CSV can be read back
        df = pd.read_csv(output_file)
        assert len(df) == 3
        assert "ASSET NAME" in df.columns

    def test_write_json_section(self, temp_dir, sample_json_data):
        input_file = temp_dir / "test_input.txt"
        input_file.write_text(sample_json_data)

        sections = parse_file(input_file)
        output_dir = temp_dir / "output"
        write_sections(sections, output_dir)

        output_file = output_dir / "logic_app_json.json"
        assert output_file.exists()

        # Verify JSON can be read back
        with open(output_file) as f:
            data = json.load(f)
        assert "$schema" in data

    def test_write_multiple_sections(
        self, temp_dir, sample_robinhood_data, sample_crypto_data
    ):
        combined_data = f"{sample_robinhood_data}\n\n{sample_crypto_data}"
        input_file = temp_dir / "test_input.txt"
        input_file.write_text(combined_data)

        sections = parse_file(input_file)
        output_dir = temp_dir / "output"
        write_sections(sections, output_dir)

        assert (output_dir / "robinhood_sales.csv").exists()
        assert (output_dir / "crypto_movements.csv").exists()

    def test_write_creates_output_directory(self, temp_dir, sample_robinhood_data):
        input_file = temp_dir / "test_input.txt"
        input_file.write_text(sample_robinhood_data)

        sections = parse_file(input_file)
        output_dir = temp_dir / "nonexistent" / "output"
        write_sections(sections, output_dir)

        assert output_dir.exists()


class TestComputeCapitalGains:
    """Test capital gains computation."""

    def test_compute_gains_basic(self, temp_dir):
        # Create a simple Robinhood CSV
        data = {
            "ASSET NAME": ["AAPL", "TSLA"],
            "RECEIVED DATE": ["2020-01-01", "2020-06-01"],
            "COST BASIS(USD)": [100.0, 200.0],
            "DATE SOLD": ["2021-01-01", "2020-12-01"],
            "PROCEEDS": [150.0, 250.0],
        }
        df = pd.DataFrame(data)
        csv_path = temp_dir / "robinhood.csv"
        df.to_csv(csv_path, index=False)

        result = compute_capital_gains(csv_path)

        assert "gain" in result.columns
        assert "days_held" in result.columns
        assert "long_term" in result.columns
        assert result.loc[0, "gain"] == 50.0
        assert result.loc[1, "gain"] == 50.0
        assert result.loc[0, "long_term"]  # held > 365 days (truthy check)
        assert not result.loc[1, "long_term"]  # held < 365 days (falsy check)

    def test_compute_gains_handles_missing_columns(self, temp_dir):
        # Create CSV with missing required columns
        data = {"ASSET NAME": ["AAPL"], "PROCEEDS": [150.0]}
        df = pd.DataFrame(data)
        csv_path = temp_dir / "incomplete.csv"
        df.to_csv(csv_path, index=False)

        result = compute_capital_gains(csv_path)

        # Should return the original dataframe without modifications
        assert "gain" not in result.columns

    def test_compute_gains_handles_invalid_data(self, temp_dir):
        # Create CSV with invalid numeric data
        data = {
            "ASSET NAME": ["AAPL", "TSLA"],
            "RECEIVED DATE": ["2020-01-01", "invalid-date"],
            "COST BASIS(USD)": [100.0, "invalid"],
            "DATE SOLD": ["2021-01-01", "2020-12-01"],
            "PROCEEDS": [150.0, 250.0],
        }
        df = pd.DataFrame(data)
        csv_path = temp_dir / "invalid.csv"
        df.to_csv(csv_path, index=False)

        result = compute_capital_gains(csv_path)

        # Should filter out invalid rows
        assert len(result) == 1


class TestIntegration:
    """Integration tests for the full workflow."""

    def test_full_workflow_with_example_dump(self, temp_dir):
        # Use the actual example_dump.txt if it exists
        example_file = Path(__file__).parent / "example_dump.txt"
        if not example_file.exists():
            pytest.skip("example_dump.txt not found")

        sections = parse_file(example_file)
        output_dir = temp_dir / "integration_output"
        write_sections(sections, output_dir)

        # Verify output files exist
        assert output_dir.exists()
        output_files = list(output_dir.glob("*"))
        assert len(output_files) > 0

    def test_end_to_end_csv_roundtrip(self, temp_dir, sample_robinhood_data):
        """Test that CSV data can be parsed and written without data loss."""
        input_file = temp_dir / "input.txt"
        input_file.write_text(sample_robinhood_data)

        sections = parse_file(input_file)
        output_dir = temp_dir / "output"
        write_sections(sections, output_dir)

        output_file = output_dir / "robinhood_sales.csv"
        df = pd.read_csv(output_file)

        # Verify all data is preserved
        assert len(df) == 3
        assert df.loc[0, "ASSET NAME"] == "AAPL"
        assert float(df.loc[0, "COST BASIS(USD)"]) == 100.0
        assert float(df.loc[0, "PROCEEDS"]) == 150.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
