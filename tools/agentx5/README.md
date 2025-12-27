# AgentX5 Multi-Dump Parser

A powerful data parsing tool that automatically splits multi-format dump files into logical datasets.

## Features

- **Automatic Section Detection**: Recognizes various data formats including:
  - Robinhood sales data (ASSET NAME, RECEIVED DATE, COST BASIS, DATE SOLD, PROCEEDS)
  - Personal finance exports (Date, Original Date, Account Type, etc.)
  - Crypto movements (Transaction, Type, Input Currency, etc.)
  - Bitcoin daily prices (Start, End, Open, High, Low, Close, Volume, Market Cap)
  - Logic-App JSON blocks
  - Scriptable JavaScript blocks

- **Smart Output**: 
  - CSV sections are automatically cleaned and formatted
  - JSON sections are pretty-printed for readability
  - Each dataset gets its own file

- **Post-Processing**:
  - Automatic capital gains computation for Robinhood data
  - Includes holding period tagging (short-term vs long-term)

- **Memory Efficient**: Streaming parser handles large files without RAM spikes

## Requirements

- Python 3.10+
- pandas

## Installation

### Quick Install

```bash
pip install -r requirements.txt
```

### Development Install

For development with testing support:

```bash
# Install with dev dependencies
pip install -e .

# Or install from requirements
pip install -r requirements.txt
```

## Usage

```bash
python multi_dump_parser.py dump.txt out_dir
```

### Arguments

- `dump.txt`: Path to your raw dump file containing mixed-format data
- `out_dir`: Directory where parsed files will be saved

## Example

```bash
# Parse a dump file
python multi_dump_parser.py my_data_dump.txt parsed_output

# Results will be saved to:
# parsed_output/robinhood_sales.csv
# parsed_output/personal_finance.csv
# parsed_output/crypto_movements.csv
# parsed_output/btc_daily_prices.csv
# parsed_output/logic_app_json.json
# parsed_output/scriptable_js.json
# parsed_output/robinhood_gains_summary.csv (if Robinhood data is present)
```

## How It Works

1. **Line-by-line scanning**: The script reads your dump file line by line
2. **Pattern matching**: When it encounters a known header pattern, it starts a new section
3. **Section collection**: Lines are collected into the appropriate section until a new header is found
4. **File generation**: Each section is written to its own clean file (CSV or JSON)
5. **Optional post-processing**: For Robinhood data, capital gains are automatically calculated

## Adding Custom Formats

To add support for additional data formats, simply extend the `HEADER_PATTERNS` dictionary in `multi_dump_parser.py`:

```python
HEADER_PATTERNS: Dict[str, re.Pattern] = {
    # Existing patterns...
    "my_custom_format": re.compile(
        r"Column1,Column2,Column3",
        re.IGNORECASE,
    ),
}
```

If your custom format should be output as JSON instead of CSV, add it to the `JSON_SECTIONS` set:

```python
JSON_SECTIONS = {"logic_app_json", "scriptable_js", "my_custom_format"}
```

## Integration with E2B

This tool is integrated with the E2B platform as an MCP server. You can use it with Claude Desktop and other AI assistants through the Model Context Protocol.

## Testing

The tool includes comprehensive unit tests and integration tests.

### Running Tests

```bash
# Run all tests
pytest test_multi_dump_parser.py -v

# Run specific test class
pytest test_multi_dump_parser.py::TestParseFile -v

# Run with coverage
pytest test_multi_dump_parser.py --cov=multi_dump_parser --cov-report=html
```

### Test Coverage

The test suite covers:
- **Parsing Tests**: All supported data formats (Robinhood, personal finance, crypto, Bitcoin prices, JSON, JavaScript)
- **Writing Tests**: CSV and JSON output generation, directory creation
- **Capital Gains Tests**: Calculation accuracy, long-term/short-term classification, error handling
- **End-to-End Tests**: Full pipeline with mixed data formats
- **Pattern Recognition Tests**: Header pattern matching and case-insensitivity

## Continuous Integration

The tool is tested on multiple platforms and Python versions via GitHub Actions:
- **Platforms**: Ubuntu, macOS, Windows
- **Python Versions**: 3.10, 3.11, 3.12

See `.github/workflows/agentx5_tests.yml` for CI configuration.

## Command-Line Interface

After installation with `pip install -e .`, you can use the tool via the CLI command:

```bash
# Using the installed command
agentx5-parser my_data_dump.txt parsed_output

# Or using python module
python -m multi_dump_parser my_data_dump.txt parsed_output
```

## License

See the main E2B repository LICENSE file.
