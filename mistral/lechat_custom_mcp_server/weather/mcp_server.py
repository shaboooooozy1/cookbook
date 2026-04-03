import os
import json
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from mistralai import Mistral

load_dotenv()

# --- MCP Server Setup ---
mcp = FastMCP(
    name="WeatherAssistant",
    host="0.0.0.0",
    port=7860,
)

# --- Mistral Client ---
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=MISTRAL_API_KEY) if MISTRAL_API_KEY else None

# --- Simulated weather data (replace with a real API in production) ---
WEATHER_DATA = {
    "paris": {"temp_c": 18, "condition": "Partly cloudy", "humidity": 65, "wind_kph": 12},
    "london": {"temp_c": 14, "condition": "Overcast", "humidity": 80, "wind_kph": 18},
    "new york": {"temp_c": 22, "condition": "Sunny", "humidity": 45, "wind_kph": 8},
    "tokyo": {"temp_c": 26, "condition": "Humid", "humidity": 75, "wind_kph": 5},
    "san francisco": {"temp_c": 16, "condition": "Foggy", "humidity": 85, "wind_kph": 20},
    "berlin": {"temp_c": 15, "condition": "Rainy", "humidity": 78, "wind_kph": 14},
    "sydney": {"temp_c": 24, "condition": "Sunny", "humidity": 50, "wind_kph": 10},
    "dubai": {"temp_c": 38, "condition": "Hot and sunny", "humidity": 30, "wind_kph": 6},
    "mumbai": {"temp_c": 32, "condition": "Humid", "humidity": 85, "wind_kph": 9},
    "toronto": {"temp_c": 12, "condition": "Partly cloudy", "humidity": 55, "wind_kph": 15},
}


def _get_weather(city: str) -> dict | None:
    """Look up simulated weather data for a city."""
    return WEATHER_DATA.get(city.lower().strip())


def _summarize_with_mistral(prompt: str) -> str:
    """Use Mistral to generate a natural-language weather summary."""
    if not client:
        return "(Mistral API key not set -- raw data returned instead)"
    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a friendly weather assistant. "
                    "Summarize the weather data in a short, helpful paragraph. "
                    "Include practical advice (umbrella, sunscreen, etc.). "
                    "Keep it under 80 words."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content


# --- MCP Tools ---


@mcp.tool()
def get_current_weather(city: str) -> dict:
    """
    Get the current weather for a city.
    Args:
        city (str): City name (e.g. "Paris", "New York")
    Returns:
        dict: Weather data including temperature, condition, humidity, and wind
    """
    data = _get_weather(city)
    if not data:
        available = ", ".join(sorted(WEATHER_DATA.keys(), key=str.title))
        return {
            "status": "error",
            "message": f"City '{city}' not found. Available cities: {available}",
        }

    return {
        "status": "success",
        "city": city.title(),
        "temperature_c": data["temp_c"],
        "temperature_f": round(data["temp_c"] * 9 / 5 + 32, 1),
        "condition": data["condition"],
        "humidity_pct": data["humidity"],
        "wind_kph": data["wind_kph"],
        "markdown": (
            f"## Weather in {city.title()}\n"
            f"| Metric | Value |\n|---|---|\n"
            f"| Temperature | {data['temp_c']}°C / {round(data['temp_c'] * 9/5 + 32, 1)}°F |\n"
            f"| Condition | {data['condition']} |\n"
            f"| Humidity | {data['humidity']}% |\n"
            f"| Wind | {data['wind_kph']} km/h |\n"
        ),
    }


@mcp.tool()
def compare_weather(city_a: str, city_b: str) -> dict:
    """
    Compare weather between two cities side by side.
    Args:
        city_a (str): First city name
        city_b (str): Second city name
    Returns:
        dict: Comparison data with markdown table
    """
    data_a = _get_weather(city_a)
    data_b = _get_weather(city_b)

    errors = []
    if not data_a:
        errors.append(f"City '{city_a}' not found.")
    if not data_b:
        errors.append(f"City '{city_b}' not found.")
    if errors:
        available = ", ".join(sorted(WEATHER_DATA.keys(), key=str.title))
        return {"status": "error", "message": " ".join(errors) + f" Available: {available}"}

    diff_c = data_a["temp_c"] - data_b["temp_c"]
    markdown = (
        f"## Weather Comparison: {city_a.title()} vs {city_b.title()}\n\n"
        f"| Metric | {city_a.title()} | {city_b.title()} |\n|---|---|---|\n"
        f"| Temperature | {data_a['temp_c']}°C | {data_b['temp_c']}°C |\n"
        f"| Condition | {data_a['condition']} | {data_b['condition']} |\n"
        f"| Humidity | {data_a['humidity']}% | {data_b['humidity']}% |\n"
        f"| Wind | {data_a['wind_kph']} km/h | {data_b['wind_kph']} km/h |\n\n"
        f"Temperature difference: **{abs(diff_c)}°C** "
        f"({'warmer' if diff_c > 0 else 'cooler'} in {city_a.title()})\n"
    )

    return {
        "status": "success",
        "city_a": city_a.title(),
        "city_b": city_b.title(),
        "temp_diff_c": diff_c,
        "markdown": markdown,
    }


@mcp.tool()
def get_weather_summary(city: str) -> dict:
    """
    Get an AI-generated natural-language weather summary with practical advice.
    Args:
        city (str): City name
    Returns:
        dict: AI-generated weather summary powered by Mistral
    """
    data = _get_weather(city)
    if not data:
        available = ", ".join(sorted(WEATHER_DATA.keys(), key=str.title))
        return {"status": "error", "message": f"City '{city}' not found. Available: {available}"}

    prompt = (
        f"Weather in {city.title()}: {data['temp_c']}°C, {data['condition']}, "
        f"{data['humidity']}% humidity, wind {data['wind_kph']} km/h."
    )
    summary = _summarize_with_mistral(prompt)

    return {
        "status": "success",
        "city": city.title(),
        "summary": summary,
    }


@mcp.tool()
def list_available_cities() -> dict:
    """
    List all cities with available weather data.
    Returns:
        dict: List of city names
    """
    cities = sorted(WEATHER_DATA.keys(), key=str.title)
    return {
        "status": "success",
        "cities": [c.title() for c in cities],
        "count": len(cities),
        "message": "Use get_current_weather(city) to check the weather for any of these cities.",
    }


@mcp.tool()
def get_travel_recommendation(cities: str) -> dict:
    """
    Get an AI-powered travel recommendation based on current weather across multiple cities.
    Args:
        cities (str): Comma-separated list of city names to evaluate
    Returns:
        dict: Travel recommendation with reasoning from Mistral AI
    """
    city_list = [c.strip() for c in cities.split(",") if c.strip()]
    if not city_list:
        return {"status": "error", "message": "Please provide at least one city."}

    weather_lines = []
    valid_cities = []
    for city in city_list:
        data = _get_weather(city)
        if data:
            valid_cities.append(city.title())
            weather_lines.append(
                f"- {city.title()}: {data['temp_c']}°C, {data['condition']}, "
                f"{data['humidity']}% humidity, wind {data['wind_kph']} km/h"
            )

    if not valid_cities:
        available = ", ".join(sorted(WEATHER_DATA.keys(), key=str.title))
        return {"status": "error", "message": f"No valid cities found. Available: {available}"}

    prompt = (
        "Given these current weather conditions, recommend the best city to visit "
        "today for outdoor activities. Explain your reasoning briefly.\n\n"
        + "\n".join(weather_lines)
    )
    recommendation = _summarize_with_mistral(prompt)

    return {
        "status": "success",
        "evaluated_cities": valid_cities,
        "recommendation": recommendation,
    }


# --- Server Execution ---
if __name__ == "__main__":
    print("Weather Assistant MCP Server starting on port 7860...")
    print("MCP Tools available:")
    print("- get_current_weather(city)")
    print("- compare_weather(city_a, city_b)")
    print("- get_weather_summary(city)")
    print("- list_available_cities()")
    print("- get_travel_recommendation(cities)")
    print()
    print("Running Weather MCP server with SSE transport")
    mcp.run(transport="sse")
