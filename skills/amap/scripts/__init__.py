"""
Amap API Toolkit
Shared utilities for Amap (AutoNavi/高德地图) API interactions
"""

import os
import getpass
from typing import Optional

AMAP_BASE_URL = "https://restapi.amap.com/v3"


def get_api_key() -> str:
    """
    Get Amap API key from environment variable or prompt user.

    Returns:
        API key string

    Raises:
        ValueError: If API key is empty
    """
    api_key = os.environ.get('AMAP_API_KEY')

    if api_key:
        return api_key

    # Prompt user for API key if not in environment
    print("AMAP_API_KEY environment variable not found.")
    api_key = getpass.getpass("Please enter your Amap API key: ")

    if not api_key:
        raise ValueError("API key cannot be empty")

    return api_key


def build_api_url(endpoint: str, params: dict) -> str:
    """
    Build Amap API URL with query parameters.

    Args:
        endpoint: API endpoint path (e.g., "/geocode/geo")
        params: Query parameters dict

    Returns:
        Full API URL with query string
    """
    from urllib.parse import urlencode

    return f"{AMAP_BASE_URL}{endpoint}?{urlencode(params)}"


def parse_coordinates(location: str) -> Optional[tuple[float, float]]:
    """
    Parse location string to coordinates.

    Args:
        location: Location string, either "longitude,latitude" or an address

    Returns:
        Tuple of (longitude, latitude) if coordinates, None otherwise
    """
    try:
        parts = location.split(',')
        if len(parts) == 2:
            lon = float(parts[0].strip())
            lat = float(parts[1].strip())
            return (lon, lat)
    except (ValueError, AttributeError):
        pass
    return None


def make_api_request(url: str, api_key: str, timeout: int = 10) -> dict:
    """
    Make HTTP request to Amap API.

    Args:
        url: Full API URL
        api_key: Amap API key
        timeout: Request timeout in seconds

    Returns:
        JSON response as dict

    Raises:
        requests.RequestException: If request fails
        ValueError: If response indicates error
    """
    import requests

    # Add key parameter to URL
    if '?' in url:
        url = f"{url}&key={api_key}"
    else:
        url = f"{url}?key={api_key}"

    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    data = response.json()

    # Check Amap API error status
    if data.get('status') != '1':
        error_code = data.get('infocode', 'UNKNOWN')
        error_msg = data.get('info', 'Unknown error')
        raise ValueError(f"Amap API Error [{error_code}]: {error_msg}")

    return data


def format_address(address_components: dict) -> str:
    """
    Format Amap address components into readable string.

    Args:
        address_components: Address components from Amap response

    Returns:
        Formatted address string
    """
    parts = [
        address_components.get('province', ''),
        address_components.get('city', ''),
        address_components.get('district', ''),
        address_components.get('street', ''),
        address_components.get('number', '')
    ]
    return ''.join([p for p in parts if p])


def geocode(address: str, city: str = None, api_key: str = None) -> dict:
    """
    Convert address to coordinates.

    Args:
        address: Address string
        city: City name (optional, improves accuracy)
        api_key: Amap API key (if None, will get from env)

    Returns:
        Geocoding result dict with coordinates
    """
    if api_key is None:
        api_key = get_api_key()

    params = {'address': address}
    if city:
        params['city'] = city

    url = build_api_url('/geocode/geo', params)
    data = make_api_request(url, api_key)

    geocodes = data.get('geocodes', [])
    if not geocodes:
        raise ValueError("No results found for the given address")

    return geocodes[0]
