#!/usr/bin/env python3
"""
Amap IP Location API Script

Converts an IP address to its geographic location.

Usage:
    python scripts/ip_location.py --ip 8.8.8.8
"""

import argparse
import sys
from typing import Optional

# Add scripts directory to path for imports
sys.path.insert(0, __file__.rsplit('/', 1)[0])

from __init__ import (
    get_api_key,
    build_api_url,
    make_api_request
)


def get_ip_location(ip: str, api_key: Optional[str] = None) -> dict:
    """
    Get geographic location from IP address.

    Args:
        ip: IP address to locate
        api_key: Amap API key (if None, will prompt)

    Returns:
        IP location result dict
    """
    if api_key is None:
        api_key = get_api_key()

    params = {'ip': ip}

    url = build_api_url('/ip', params)
    data = make_api_request(url, api_key)

    return data


def format_ip_location_result(data: dict) -> str:
    """Format IP location result for display."""
    province = data.get('province', 'N/A')
    city = data.get('city', 'N/A')
    ip = data.get('ip', 'N/A')
    rectangle = data.get('rectangle', 'N/A')

    output = []
    output.append(f"IP Address: {ip}")
    output.append(f"Province: {province}")
    output.append(f"City: {city}")
    if rectangle != 'N/A':
        output.append(f"Rectangle: {rectangle}")

    return '\n'.join(output)


def main():
    parser = argparse.ArgumentParser(
        description='Amap IP Location - Convert IP address to geographic location',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Locate an IP address
  python scripts/ip_location.py --ip 8.8.8.8

  # Locate a Chinese IP address
  python scripts/ip_location.py --ip 114.114.114.114
        """
    )

    parser.add_argument('--ip', type=str, required=True,
                        help='IP address to locate')

    args = parser.parse_args()

    try:
        result = get_ip_location(args.ip)
        print(format_ip_location_result(result))

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
