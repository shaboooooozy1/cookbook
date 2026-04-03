# Custom MCP Servers for LeChat

This directory contains example [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) servers designed to work with [LeChat](https://chat.mistral.ai), Mistral's chat interface.

MCP servers expose **tools** that LeChat can call during a conversation, letting you extend LeChat with custom functionality -- games, data lookups, note-taking, and more.

## Examples

| Server | Description | Tools |
|---|---|---|
| [tic-tac-toe](./tic-tac-toe/) | Play tic-tac-toe against Mistral AI with trash talk | `create_room`, `make_move`, `send_chat`, `get_room_state`, `list_rooms`, `get_help` |
| [weather](./weather/) | Weather lookups, comparisons, and AI-powered travel recommendations | `get_current_weather`, `compare_weather`, `get_weather_summary`, `list_available_cities`, `get_travel_recommendation` |
| [notes](./notes/) | AI-powered note-taking with summarization, action items, and auto-tagging | `create_note`, `get_note`, `update_note`, `delete_note`, `list_notes`, `search_notes`, `summarize_note`, `generate_action_items`, `suggest_tags` |

## How It Works

```
LeChat  <--SSE-->  Your MCP Server (hosted on HF Spaces, etc.)
                        |
                   Mistral API (for AI features)
```

1. You deploy an MCP server that exposes tools via SSE transport
2. In LeChat, add the server URL under **Settings > MCP Servers**
3. When you chat, LeChat discovers the available tools and calls them as needed

## Common Stack

All examples use:
- **[FastMCP](https://github.com/jlowin/fastmcp)** -- Python framework for building MCP servers
- **[Mistral AI SDK](https://github.com/mistralai/client-python)** -- for AI-powered tool logic
- **SSE transport** -- the protocol LeChat uses to communicate with MCP servers

## Quick Start

Each example can be run locally:

```bash
cd <server-directory>
pip install -r requirements.txt
export MISTRAL_API_KEY="your-key"
python mcp_server.py
```

Or deployed to [Hugging Face Spaces](https://huggingface.co/spaces) using the included `Dockerfile`.

## Building Your Own

1. Create a new directory under `lechat_custom_mcp_server/`
2. Use `FastMCP` to define your tools (see any example for the pattern)
3. Add a `requirements.txt` with pinned versions
4. Add a `Dockerfile` for deployment
5. Deploy and connect to LeChat

See the [tic-tac-toe README](./tic-tac-toe/README.md) for a detailed end-to-end walkthrough.
