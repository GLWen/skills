#!/usr/bin/env python3
"""
Amap Geocoding API Script

Converts addresses to coordinates (geocoding) and coordinates to addresses (reverse geocoding).

Usage:
    # Forward geocoding (address to coordinates)
    python scripts/geocoding.py --address "北京市朝阳区阜通东大街6号" --city "北京市"

    # Reverse geocoding (coordinates to address)
    python scripts/geocoding.py --longitude 116.481485 --latitude 39.990464
"""

import argparse
import sys
from typing import Optional

# Add scripts directory to path for imports
sys.path.insert(0, __file__.rsplit('/', 1)[0])

from __init__ import (
    get_api_key,
    build_api_url,
    make_api_request,
    format_address
)


def geocode(address: str, city: Optional[str] = None, api_key: Optional[str] = None) -> dict:
    """
    Convert address to coordinates.

    Args:
        address: Address string
        city: City name (optional, improves accuracy)
        api_key: Amap API key (if None, will prompt)

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


def reverse_geocode(longitude: float, latitude: float, api_key: Optional[str] = None) -> dict:
    """
    Convert coordinates to address.

    Args:
        longitude: Longitude
        latitude: Latitude
        api_key: Amap API key (if None, will prompt)

    Returns:
        Reverse geocoding result dict with address info
    """
    if api_key is None:
        api_key = get_api_key()

    params = {
        'location': f'{longitude},{latitude}',
        'extensions': 'base'  # Use 'all' for detailed info
    }

    url = build_api_url('/geocode/regeo', params)
    data = make_api_request(url, api_key)

    regeocode = data.get('regeocode')
    if not regeocode:
        raise ValueError("No results found for the given coordinates")

    return regeocode


def format_geocode_result(result: dict) -> str:
    """Format geocoding result for display."""
    location = result.get('location', '')
    formatted_address = result.get('formatted_address', '')
    level = result.get('level', '')
    province = result.get('province', '')
    city = result.get('city', '')
    district = result.get('district', '')

    output = []
    output.append(f"Address: {formatted_address}")
    output.append(f"Coordinates: {location}")
    output.append(f"Level: {level}")
    if province:
        output.append(f"Province: {province}")
    if city:
        output.append(f"City: {city}")
    if district:
        output.append(f"District: {district}")

    return '\n'.join(output)


def format_reverse_geocode_result(result: dict) -> str:
    """Format reverse geocoding result for display."""
    address_component = result.get('addressComponent', {})
    formatted_address = result.get('formatted_address', '')

    output = []
    output.append(f"Address: {formatted_address}")
    output.append(f"Province: {address_component.get('province', '')}")
    output.append(f"City: {address_component.get('city', '')}")
    output.append(f"District: {address_component.get('district', '')}")
    output.append(f"Street: {address_component.get('street', '')}")
    output.append(f"Street Number: {address_component.get('streetNumber', '')}")

    return '\n'.join(output)


def main():
    parser = argparse.ArgumentParser(
        description='Amap Geocoding - Convert addresses to coordinates and vice versa',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Forward geocoding (address to coordinates)
  python scripts/geocoding.py --address "北京市朝阳区阜通东大街6号" --city "北京市"

  # Reverse geocoding (coordinates to address)
  python scripts/geocoding.py --longitude 116.481485 --latitude 39.990464
        """
    )

    # Forward geocoding parameters
    parser.add_argument('--address', type=str, help='Address string to geocode')
    parser.add_argument('--city', type=str, help='City name (optional, improves accuracy)')

    # Reverse geocoding parameters
    parser.add_argument('--longitude', type=float, help='Longitude for reverse geocoding')
    parser.add_argument('--latitude', type=float, help='Latitude for reverse geocoding')

    args = parser.parse_args()

    # Validate arguments
    if args.address and (args.longitude is not None or args.latitude is not None):
        parser.error("Cannot use both address and coordinates. Use either --address OR (--longitude AND --latitude)")

    if not args.address and (args.longitude is None or args.latitude is None):
        parser.error("Please provide either --address OR both --longitude and --latitude")

    try:
        if args.address:
            # Forward geocoding
            result = geocode(args.address, args.city)
            print(format_geocode_result(result))
        else:
            # Reverse geocoding
            result = reverse_geocode(args.longitude, args.latitude)
            print(format_reverse_geocode_result(result))

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
