"""
Travel Planner - Weather Service
Fetches weather forecasts for travel destinations.
"""

import json
import urllib.request
from typing import Optional
from .api_config import get_api_key, get_endpoint


def get_weather(city: str, city_adcode: str = None) -> dict:
    """
    Get current weather and forecast for a city.

    Args:
        city: City name
        city_adcode: City administrative code (optional)

    Returns:
        Weather data dict
    """
    key = get_api_key("amap")
    if not key:
        return {"error": "API key not configured"}

    params = {
        "city": city,
        "extensions": "all",  # Get forecast too
        "output": "json"
    }

    if city_adcode:
        params["city_adcode"] = city_adcode

    url = get_endpoint("amap_weather", params)

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            return parse_weather_response(data)
    except Exception as e:
        return {"error": str(e)}


def parse_weather_response(data: dict) -> dict:
    """Parse Amap weather API response."""
    if data.get("status") != "1":
        return {"error": data.get("info", "Unknown error")}

    result = {
        "province": data.get("province", ""),
        "city": data.get("city", ""),
        "adcode": data.get("adcode", ""),
        "report_time": data.get("report_time", ""),
        "current": {},
        "forecast": []
    }

    # Current weather
    lives = data.get("lives", [])
    if lives:
        live = lives[0]
        result["current"] = {
            "temperature": live.get("temperature", ""),
            "humidity": live.get("humidity", ""),
            "wind_direction": live.get("winddirection", ""),
            "wind_power": live.get("windpower", ""),
            "weather": live.get("weather", ""),
        }

    # Forecast
    forecasts = data.get("forecasts", [])
    if forecasts:
        for cast in forecasts[0].get("casts", []):
            result["forecast"].append({
                "date": cast.get("date", ""),
                "week": cast.get("week", ""),
                "day_weather": cast.get("dayweather", ""),
                "night_weather": cast.get("nightweather", ""),
                "day_temp": cast.get("daytemp", ""),
                "night_temp": cast.get("nighttemp", ""),
                "day_wind": cast.get("daywind", ""),
                "night_wind": cast.get("nightwind", ""),
            })

    return result


def format_weather_summary(weather_data: dict) -> str:
    """Format weather data for display."""
    if "error" in weather_data:
        return f"无法获取天气信息: {weather_data['error']}"

    lines = [f"### {weather_data['city']} 天气预报"]

    if weather_data.get("report_time"):
        lines.append(f"*发布时间: {weather_data['report_time']}*")

    current = weather_data.get("current", {})
    if current:
        lines.append("")
        lines.append("#### 当前天气")
        lines.append(f"- 天气: {current.get('weather', 'N/A')}")
        lines.append(f"- 温度: {current.get('temperature', 'N/A')}°C")
        lines.append(f"- 湿度: {current.get('humidity', 'N/A')}%")
        lines.append(f"- 风向: {current.get('wind_direction', 'N/A')} {current.get('wind_power', '')}级")

    forecast = weather_data.get("forecast", [])
    if forecast:
        lines.append("")
        lines.append("#### 天气预报")
        for day in forecast[:7]:
            lines.append(f"- **{day['date']} ({day['week']})}**: "
                        f"{day['day_weather']} → {day['night_weather']}, "
                        f"{day['night_temp']}°C ~ {day['day_temp']}°C")

    return "\n".join(lines)
