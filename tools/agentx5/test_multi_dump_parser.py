"""
Test suite for the AgentX5 Multi-Dump Parser
"""
import csv
import json
import tempfile
from pathlib import Path
import pytest
import pandas as pd

from multi_dump_parser import (
    parse_file,
    write_sections,
    compute_capital_gains,
    HEADER_PATTERNS,
)


class TestParseFile:
    """Test the parse_file function"""

    def test_parse_robinhood_data(self, tmp_path):
        """Test parsing Robinhood sales data"""
        dump_content = """ASSET NAME,RECEIVED DATE,COST BASIS(USD),DATE SOLD,PROCEEDS
AAPL,2023-01-15,1000.00,2023-06-20,1500.00
GOOGL,2023-02-10,2000.00,2023-07-15,2300.00
"""
        dump_file = tmp_path / "test_dump.txt"
        dump_file.write_text(dump_content)

        sections = parse_file(dump_file)

        assert "robinhood_sales" in sections
        assert len(sections["robinhood_sales"]) == 3
        assert sections["robinhood_sales"][0].startswith("ASSET NAME")

    def test_parse_personal_finance_data(self, tmp_path):
        """Test parsing personal finance data"""
        dump_content = """Date,Original Date,Account Type,Account Name,Account Number,Institution Name
2023-01-01,2023-01-01,Checking,Main Account,1234,Bank of America
2023-01-02,2023-01-02,Savings,Savings Account,5678,Chase
"""
        dump_file = tmp_path / "test_dump.txt"
        dump_file.write_text(dump_content)

        sections = parse_file(dump_file)

        assert "personal_finance" in sections
        assert len(sections["personal_finance"]) == 3

    def test_parse_crypto_movements(self, tmp_path):
        """Test parsing crypto movements data"""
        dump_content = """Transaction,Type,Input Currency,Input Amount,Output Currency
TX001,Buy,USD,1000,BTC
TX002,Sell,BTC,0.5,USD
"""
        dump_file = tmp_path / "test_dump.txt"
        dump_file.write_text(dump_content)

        sections = parse_file(dump_file)

        assert "crypto_movements" in sections
        assert len(sections["crypto_movements"]) == 3

    def test_parse_btc_daily_prices(self, tmp_path):
        """Test parsing Bitcoin daily prices"""
        dump_content = """Start,End,Open,High,Low,Close,Volume,Market Cap
2023-01-01,2023-01-01,30000,31000,29500,30500,1000000,500000000
2023-01-02,2023-01-02,30500,31500,30000,31000,1100000,510000000
"""
        dump_file = tmp_path / "test_dump.txt"
        dump_file.write_text(dump_content)

        sections = parse_file(dump_file)

        assert "btc_daily_prices" in sections
        assert len(sections["btc_daily_prices"]) == 3

    def test_parse_logic_app_json(self, tmp_path):
        """Test parsing Logic App JSON"""
        json_content = '{"$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#", "contentVersion": "1.0.0.0"}'
        dump_file = tmp_path / "test_dump.txt"
        dump_file.write_text(json_content)

        sections = parse_file(dump_file)

        assert "logic_app_json" in sections
        assert len(sections["logic_app_json"]) == 1

    def test_parse_scriptable_js(self, tmp_path):
        """Test parsing Scriptable JavaScript"""
        js_content = """// Variables used by Scriptable.
// These must be at the very top of the file. Do not edit.
let widget = new ListWidget()
widget.addText("Hello World")
"""
        dump_file = tmp_path / "test_dump.txt"
        dump_file.write_text(js_content)

        sections = parse_file(dump_file)

        assert "scriptable_js" in sections
        assert len(sections["scriptable_js"]) == 4

    def test_parse_multiple_sections(self, tmp_path):
        """Test parsing file with multiple sections"""
        dump_content = """ASSET NAME,RECEIVED DATE,COST BASIS(USD),DATE SOLD,PROCEEDS
AAPL,2023-01-15,1000.00,2023-06-20,1500.00

Date,Original Date,Account Type,Account Name,Account Number,Institution Name
2023-01-01,2023-01-01,Checking,Main Account,1234,Bank of America

Transaction,Type,Input Currency,Input Amount,Output Currency
TX001,Buy,USD,1000,BTC
"""
        dump_file = tmp_path / "test_dump.txt"
        dump_file.write_text(dump_content)

        sections = parse_file(dump_file)

        assert len(sections) == 3
        assert "robinhood_sales" in sections
        assert "personal_finance" in sections
        assert "crypto_movements" in sections


class TestWriteSections:
    """Test the write_sections function"""

    def test_write_csv_section(self, tmp_path):
        """Test writing CSV sections"""
        sections = {
            "robinhood_sales": [
                "ASSET NAME,RECEIVED DATE,COST BASIS(USD),DATE SOLD,PROCEEDS",
                "AAPL,2023-01-15,1000.00,2023-06-20,1500.00",
                "GOOGL,2023-02-10,2000.00,2023-07-15,2300.00",
            ]
        }

        write_sections(sections, tmp_path)

        output_file = tmp_path / "robinhood_sales.csv"
        assert output_file.exists()

        df = pd.read_csv(output_file)
        assert len(df) == 2
        assert "ASSET NAME" in df.columns

    def test_write_json_section(self, tmp_path):
        """Test writing JSON sections"""
        sections = {
            "logic_app_json": [
                '{"$schema": "test", "contentVersion": "1.0.0.0"}'
            ]
        }

        write_sections(sections, tmp_path)

        output_file = tmp_path / "logic_app_json.json"
        assert output_file.exists()

        with open(output_file) as f:
            data = json.load(f)
            assert data["$schema"] == "test"
            assert data["contentVersion"] == "1.0.0.0"

    def test_write_empty_section(self, tmp_path):
        """Test writing empty CSV section"""
        sections = {
            "robinhood_sales": [
                "ASSET NAME,RECEIVED DATE,COST BASIS(USD),DATE SOLD,PROCEEDS"
            ]
        }

        write_sections(sections, tmp_path)

        output_file = tmp_path / "robinhood_sales.csv"
        assert output_file.exists()

        df = pd.read_csv(output_file)
        assert len(df) == 0
        assert "ASSET NAME" in df.columns

    def test_write_creates_directory(self, tmp_path):
        """Test that write_sections creates output directory if it doesn't exist"""
        output_dir = tmp_path / "nested" / "output"
        sections = {
            "robinhood_sales": [
                "ASSET NAME,RECEIVED DATE,COST BASIS(USD),DATE SOLD,PROCEEDS",
                "AAPL,2023-01-15,1000.00,2023-06-20,1500.00",
            ]
        }

        write_sections(sections, output_dir)

        assert output_dir.exists()
        assert (output_dir / "robinhood_sales.csv").exists()


class TestCapitalGains:
    """Test the compute_capital_gains function"""

    def test_compute_capital_gains_basic(self, tmp_path):
        """Test basic capital gains computation"""
        csv_content = """ASSET NAME,RECEIVED DATE,COST BASIS(USD),DATE SOLD,PROCEEDS
AAPL,2023-01-15,1000.00,2023-06-20,1500.00
GOOGL,2023-02-10,2000.00,2023-07-15,2300.00
"""
        csv_file = tmp_path / "robinhood_sales.csv"
        csv_file.write_text(csv_content)

        gains_df = compute_capital_gains(csv_file)

        assert "gain" in gains_df.columns
        assert "days_held" in gains_df.columns
        assert "long_term" in gains_df.columns
        assert len(gains_df) == 2

        # Check calculated gains
        assert gains_df.iloc[0]["gain"] == 500.00  # AAPL
        assert gains_df.iloc[1]["gain"] == 300.00  # GOOGL

    def test_compute_capital_gains_long_term(self, tmp_path):
        """Test long-term capital gains detection"""
        csv_content = """ASSET NAME,RECEIVED DATE,COST BASIS(USD),DATE SOLD,PROCEEDS
AAPL,2022-01-15,1000.00,2023-06-20,1500.00
GOOGL,2023-02-10,2000.00,2023-07-15,2300.00
"""
        csv_file = tmp_path / "robinhood_sales.csv"
        csv_file.write_text(csv_content)

        gains_df = compute_capital_gains(csv_file)

        # First sale is long-term (>365 days), second is short-term
        assert gains_df.iloc[0]["long_term"] == True
        assert gains_df.iloc[1]["long_term"] == False

    def test_compute_capital_gains_with_invalid_data(self, tmp_path):
        """Test capital gains computation handles invalid data"""
        csv_content = """ASSET NAME,RECEIVED DATE,COST BASIS(USD),DATE SOLD,PROCEEDS
AAPL,2023-01-15,1000.00,2023-06-20,1500.00
GOOGL,invalid-date,2000.00,2023-07-15,2300.00
MSFT,2023-03-10,abc,2023-08-15,3300.00
"""
        csv_file = tmp_path / "robinhood_sales.csv"
        csv_file.write_text(csv_content)

        gains_df = compute_capital_gains(csv_file)

        # Only valid row should be included
        assert len(gains_df) == 1
        assert gains_df.iloc[0]["ASSET NAME"] == "AAPL"

    def test_compute_capital_gains_missing_columns(self, tmp_path):
        """Test capital gains computation with missing columns"""
        csv_content = """ASSET NAME,RECEIVED DATE
AAPL,2023-01-15
"""
        csv_file = tmp_path / "robinhood_sales.csv"
        csv_file.write_text(csv_content)

        gains_df = compute_capital_gains(csv_file)

        # Should return original dataframe when required columns are missing
        assert "gain" not in gains_df.columns


class TestEndToEnd:
    """End-to-end integration tests"""

    def test_full_pipeline_with_example_data(self, tmp_path):
        """Test the full pipeline with example dump data"""
        dump_content = """ASSET NAME,RECEIVED DATE,COST BASIS(USD),DATE SOLD,PROCEEDS
AAPL,2023-01-15,1000.00,2023-06-20,1500.00
GOOGL,2023-02-10,2000.00,2023-07-15,2300.00

Date,Original Date,Account Type,Account Name,Account Number,Institution Name
2023-01-01,2023-01-01,Checking,Main Account,1234,Bank of America

Transaction,Type,Input Currency,Input Amount,Output Currency
TX001,Buy,USD,1000,BTC

Start,End,Open,High,Low,Close,Volume,Market Cap
2023-01-01,2023-01-01,30000,31000,29500,30500,1000000,500000000

{"$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#", "contentVersion": "1.0.0.0"}

// Variables used by Scriptable.
let widget = new ListWidget()
"""
        dump_file = tmp_path / "dump.txt"
        dump_file.write_text(dump_content)

        output_dir = tmp_path / "output"

        # Parse and write sections
        sections = parse_file(dump_file)
        write_sections(sections, output_dir)

        # Verify all expected files were created
        assert (output_dir / "robinhood_sales.csv").exists()
        assert (output_dir / "personal_finance.csv").exists()
        assert (output_dir / "crypto_movements.csv").exists()
        assert (output_dir / "btc_daily_prices.csv").exists()
        assert (output_dir / "logic_app_json.json").exists()
        assert (output_dir / "scriptable_js.json").exists()

        # Compute capital gains
        robinhood_file = output_dir / "robinhood_sales.csv"
        gains_df = compute_capital_gains(robinhood_file)
        gains_df.to_csv(output_dir / "robinhood_gains_summary.csv", index=False)

        assert (output_dir / "robinhood_gains_summary.csv").exists()

        # Verify gains calculations
        assert len(gains_df) == 2
        assert "gain" in gains_df.columns
        assert "long_term" in gains_df.columns


class TestHeaderPatterns:
    """Test header pattern recognition"""

    def test_all_header_patterns_are_valid(self):
        """Test that all header patterns compile correctly"""
        for name, pattern in HEADER_PATTERNS.items():
            assert pattern is not None
            # Test that pattern can match
            if name == "robinhood_sales":
                assert pattern.search("ASSET NAME,RECEIVED DATE,COST BASIS(USD),DATE SOLD,PROCEEDS")
            elif name == "personal_finance":
                assert pattern.search("Date,Original Date,Account Type,Account Name,Account Number,Institution Name")
            elif name == "crypto_movements":
                assert pattern.search("Transaction,Type,Input Currency,Input Amount,Output Currency")
            elif name == "btc_daily_prices":
                assert pattern.search("Start,End,Open,High,Low,Close,Volume,Market Cap")

    def test_header_patterns_case_insensitive(self):
        """Test that header patterns are case-insensitive"""
        # Robinhood pattern should match lowercase
        assert HEADER_PATTERNS["robinhood_sales"].search(
            "asset name,received date,cost basis(usd),date sold,proceeds"
        )

        # Personal finance pattern should match mixed case
        assert HEADER_PATTERNS["personal_finance"].search(
            "date,original date,account type,account name,account number,institution name"
        )
