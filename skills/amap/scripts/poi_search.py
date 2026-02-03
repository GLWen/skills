#!/usr/bin/env python3
"""
Amap POI Search API Script

Searches for Points of Interest around a specified location.

Usage:
    # Search around city center
    python scripts/poi_search.py --keywords "餐厅" --city "北京市" --radius 2000

    # Search around specific coordinates
    python scripts/poi_search.py --keywords "加油站" --longitude 116.481485 --latitude 39.990464 --city "北京市" --radius 500
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


def search_poi(keywords: str, city: str, longitude: Optional[float] = None,
               latitude: Optional[float] = None, radius: int = 1000,
               api_key: Optional[str] = None) -> dict:
    """
    Search for Points of Interest.

    Args:
        keywords: Search keywords
        city: City name (required)
        longitude: Center longitude (optional, defaults to city center)
        latitude: Center latitude (optional, defaults to city center)
        radius: Search radius in meters (default: 1000)
        api_key: Amap API key (if None, will prompt)

    Returns:
        POI search result dict
    """
    if api_key is None:
        api_key = get_api_key()

    params = {
        'keywords': keywords,
        'city': city,
        'radius': radius
    }

    if longitude is not None and latitude is not None:
        params['location'] = f'{longitude},{latitude}'

    url = build_api_url('/place/text', params)
    data = make_api_request(url, api_key)

    pois = data.get('pois', [])
    if not pois:
        raise ValueError("No POIs found")

    return data


def format_poi_result(data: dict, limit: int = 10) -> str:
    """
    Format POI search result for display.

    Args:
        data: POI search result data
        limit: Maximum number of results to display

    Returns:
        Formatted result string
    """
    pois = data.get('pois', [])
    count = int(data.get('count', 0))
    total = min(count, len(pois))

    output = []
    output.append(f"Found {count} POIs (showing {min(total, limit)}):")
    output.append("=" * 60)

    for i, poi in enumerate(pois[:limit], 1):
        name = poi.get('name', 'N/A')
        address = poi.get('address', 'N/A')
        location = poi.get('location', 'N/A')
        distance = poi.get('distance', 0)
        tel = poi.get('tel', 'N/A')
        ptype = poi.get('type', 'N/A')

        output.append(f"\n{i}. {name}")
        output.append(f"   Address: {address}")
        output.append(f"   Location: {location}")
        output.append(f"   Distance: {distance}m")
        if tel and tel != '[]':
            output.append(f"   Phone: {tel}")
        if ptype:
            output.append(f"   Type: {ptype}")

    if count > limit:
        output.append(f"\n... and {count - limit} more results")

    return '\n'.join(output)


def main():
    parser = argparse.ArgumentParser(
        description='Amap POI Search - Search for Points of Interest',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search around city center
  python scripts/poi_search.py --keywords "餐厅" --city "北京市" --radius 2000

  # Search around specific coordinates
  python scripts/poi_search.py --keywords "加油站" --longitude 116.481485 --latitude 39.990464 --city "北京市" --radius 500

  # Search with keywords and type
  python scripts/poi_search.py --keywords "星巴克" --city "上海市" --radius 1000
        """
    )

    parser.add_argument('--keywords', type=str, required=True,
                        help='Search keywords')
    parser.add_argument('--city', type=str, required=True,
                        help='City name (required)')
    parser.add_argument('--longitude', type=float,
                        help='Center longitude (optional, defaults to city center)')
    parser.add_argument('--latitude', type=float,
                        help='Center latitude (optional, defaults to city center)')
    parser.add_argument('--radius', type=int, default=1000,
                        help='Search radius in meters (default: 1000)')
    parser.add_argument('--limit', type=int, default=10,
                        help='Maximum number of results to display (default: 10)')

    args = parser.parse_args()

    # Validate coordinates
    if (args.longitude is not None) != (args.latitude is not None):
        parser.error("Both --longitude and --latitude must be provided together")

    try:
        result = search_poi(
            keywords=args.keywords,
            city=args.city,
            longitude=args.longitude,
            latitude=args.latitude,
            radius=args.radius
        )
        print(format_poi_result(result, limit=args.limit))

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
