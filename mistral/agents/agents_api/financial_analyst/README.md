# Financial Analyst with MistralAI Agents API and MCP

A financial analysis application that uses MistralAI agents API with MCP servers for stock analysis and report generation.

[![Financial Analyst Demo](https://raw.githubusercontent.com/mistralai/cookbook/refs/heads/main/gif/financial_analyst.gif)](https://www.youtube.com/watch?v=ocxRKz73UJw)

## Use Case

- Get real-time stock prices, historical data and analyst recommendations
- Generate comprehensive financial reports
- Save reports to files

## Architecture

```
├── mcp_servers/
│   ├── stdio_yfinance_server.py
│   ├── stdio_report_gen_server.py
│   └── stdio_save_report_server.py
├── async_run_report_gen_mcp.py
```

### Main Application
- **app.py**: Chainlit interface with MistralAI agent integration

### MCP Servers
- **stdio_yfinance_server.py**: Yahoo Finance data retrieval (prices, financials)
- **stdio_report_gen_server.py**: LLM-powered report generation using MistralAI
- **stdio_save_report_server.py**: Report persistence to files

## Installation

```bash
pip install chainlit yfinance mcp mistralai loguru griffe
```

## Environment Setup

Set your MistralAI API key as an environment variable (the app forwards it to the MCP servers it spawns; nothing needs to be pasted into source files):
```bash
export MISTRAL_API_KEY="your_api_key_here"
```

## Usage

Run the application:
```bash
chainlit run app.py
```

Open your browser and ask questions like:
- "What's the current stock price of AAPL?"
- "Get me a report on the historical stock prices of microsoft and save it to msft_historical.md"
- "Show me Microsoft's analyst recommendations"

The app will automatically use the appropriate MCP servers to fetch data and generate reports. Saved reports land in the `reports/` directory next to `app.py` (only `.md` / `.txt` file names are accepted).
