# Weather Assistant MCP Server for LeChat

A custom MCP server that provides weather information and AI-powered travel recommendations directly inside LeChat.

## What You'll Create

A weather assistant that can:
- Look up current weather conditions for cities worldwide
- Compare weather between two cities side by side
- Generate AI-powered weather summaries with practical advice (powered by Mistral)
- Recommend the best city to visit based on current conditions

## Architecture

```
LeChat <-> SSE Transport <-> Weather MCP Server <-> Mistral AI (summaries)
```

## Project Structure

```
weather/
├── mcp_server.py      # MCP server with weather tools
├── requirements.txt   # Pinned Python dependencies
├── Dockerfile         # For Hugging Face Spaces deployment
└── README.md          # This file
```

## MCP Tools

| Tool | Description |
|---|---|
| `get_current_weather(city)` | Get temperature, condition, humidity, and wind for a city |
| `compare_weather(city_a, city_b)` | Side-by-side weather comparison table |
| `get_weather_summary(city)` | AI-generated natural-language summary with advice |
| `list_available_cities()` | List all cities with weather data |
| `get_travel_recommendation(cities)` | AI-powered best-city-to-visit recommendation |

## Prerequisites

- Python 3.11+
- A [Mistral API key](https://console.mistral.ai) (for AI-powered summaries)

## Local Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set your Mistral API key
export MISTRAL_API_KEY="your-api-key-here"

# Set the shared secret that clients must send as `Authorization: Bearer <token>`
export MCP_AUTH_TOKEN="$(openssl rand -hex 32)"

# Run the MCP server
python mcp_server.py
```

The server starts on port 7860 with SSE transport. It refuses to start if `MCP_AUTH_TOKEN` is unset, and answers `401` to any request to `/sse` or `/messages` that does not carry the token.

## Deploy to Hugging Face Spaces

> **Warning:** without the bearer token, the `/sse` endpoint is callable by anyone who knows the Space URL and every AI-powered tool call bills your Mistral API key. Keep `MCP_AUTH_TOKEN` secret and consider making the Space private.

1. Create a new Space on [Hugging Face](https://huggingface.co/spaces) with **Docker** SDK
2. Upload the project files
3. Add `MISTRAL_API_KEY` and `MCP_AUTH_TOKEN` as Space secrets
4. The Space will build and run automatically

## Connect to LeChat

1. Open [LeChat](https://chat.mistral.ai)
2. Go to **Settings > MCP Servers**
3. Add your deployed server URL (e.g., `https://your-space.hf.space/sse`) and configure the connector with the header `Authorization: Bearer <MCP_AUTH_TOKEN>`
4. Start chatting! Try: *"What's the weather in Paris?"*

## Extending This Example

This example uses simulated weather data. To use real data, replace the `WEATHER_DATA` dictionary and `_get_weather()` function with calls to a real weather API such as:
- [OpenWeatherMap](https://openweathermap.org/api)
- [WeatherAPI](https://www.weatherapi.com/)
- [Open-Meteo](https://open-meteo.com/) (free, no API key required)

## Author

Mistral AI Cookbook
