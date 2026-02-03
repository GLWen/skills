"""
Travel Planner - API Configuration Manager
Manages API keys and service configuration for travel planning.
"""

import os
import json
from pathlib import Path

# Default config file location
CONFIG_DIR = Path.home() / ".config" / "travel-planner"
CONFIG_FILE = CONFIG_DIR / "config.json"


def ensure_config_dir():
    """Ensure config directory exists."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config():
    """Load configuration from file."""
    ensure_config_dir()
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_config(config):
    """Save configuration to file."""
    ensure_config_dir()
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def get_api_key(service: str) -> str:
    """Get API key for a service."""
    config = load_config()
    return config.get(service, "")


def set_api_key(service: str, key: str) -> None:
    """Set API key for a service."""
    config = load_config()
    config[service] = key
    save_config(config)


def check_api_keys() -> dict:
    """Check which API keys are configured."""
    config = load_config()
    services = {
        "amap": "高德地图 (POI搜索、路线规划、地理编码)",
        "weather": "高德天气 (天气预报)",
    }
    status = {}
    for service, description in services.items():
        key = config.get(service, "")
        status[service] = {
            "name": description,
            "configured": bool(key),
            "key_preview": key[:4] + "..." if key else ""
        }
    return status


def prompt_user_for_api_keys():
    """Return prompt text for user to input API keys."""
    return """
## 需要配置 API 密钥

为了提供完整功能，请配置以下 API 密钥：

### 高德地图 API (必需)
- 用途: POI搜索、路线规划、地理编码、天气查询
- 申请地址: https://lbs.amap.com/api
- 启用服务: 搜索服务、路线规划、地理/逆地理编码、天气查询

### 获取密钥后，请提供：
1. 高德地图 Web服务 API Key
2. (可选) 其他服务的 API Key

或者直接告诉我，我会在生成攻略时使用占位符。
"""


# API Endpoints
API_ENDPOINTS = {
    "amap_geocode": "https://restapi.amap.com/v3/geocode/geo",
    "amap_poi": "https://restapi.amap.com/v3/place/text",
    "amap_route_driving": "https://restapi.amap.com/v3/direction/driving",
    "amap_route_transit": "https://restapi.amap.com/v3/direction/transit/integrated",
    "amap_weather": "https://restapi.amap.com/v3/weather/weatherInfo",
}


def get_endpoint(service: str, params: dict = None) -> str:
    """Build full API URL with query parameters."""
    base_url = API_ENDPOINTS.get(service, "")
    if not params:
        return base_url

    key = get_api_key("amap")
    if key:
        params["key"] = key

    query = "&".join([f"{k}={v}" for k, v in params.items()])
    return f"{base_url}?{query}"
