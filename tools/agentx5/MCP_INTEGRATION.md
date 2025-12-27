# AgentX5 MCP Server Integration

## Overview

The AgentX5 Multi-Dump Parser is integrated with the E2B platform as an MCP (Model Context Protocol) server. This allows AI assistants like Claude Desktop to use the parser as a tool for processing multi-format data dumps.

## MCP Server Registration

The AgentX5 server is registered in the E2B MCP server registry at `spec/mcp-server.json`:

```json
{
  "agentx5": {
    "title": "AgentX5 Multi-Dump Parser",
    "description": "A powerful data parsing tool that automatically splits multi-format dump files into logical datasets...",
    "type": "object",
    "x-dockerHubUrl": "https://hub.docker.com/mcp/server/agentx5-multi-dump-parser/overview"
  }
}
```

## Using AgentX5 with Claude Desktop

To use the AgentX5 parser with Claude Desktop via MCP:

1. Ensure you have Claude Desktop installed
2. The AgentX5 server should be available through the E2B MCP server registry
3. You can then ask Claude to parse data dump files using natural language

Example prompts:
- "Parse this mixed-format data dump and separate it into different datasets"
- "Calculate capital gains from this Robinhood sales data"
- "Extract Bitcoin price data from this dump file"

## Supported Data Formats

The parser automatically detects and separates:

- **Robinhood Sales Data**: Stock transactions with automatic capital gains calculations
- **Personal Finance Exports**: Bank account and transaction data
- **Crypto Movements**: Cryptocurrency transaction history
- **Bitcoin Daily Prices**: Historical BTC market data
- **Logic App JSON**: Azure Logic App workflow definitions
- **Scriptable JavaScript**: iOS Scriptable widget code

## Docker Integration

For E2B sandbox integration, the tool can be packaged as a Docker container:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "multi_dump_parser.py"]
```

## API Integration

When used through MCP, the tool exposes these capabilities:

- `parse_dump`: Parse a multi-format dump file
- `compute_gains`: Calculate capital gains from Robinhood data
- `list_sections`: List detected sections in a dump file
- `get_section`: Retrieve a specific parsed section

## Development

See the main README.md for development and testing instructions.
