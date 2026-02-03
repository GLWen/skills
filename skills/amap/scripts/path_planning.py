#!/usr/bin/env python3
"""
Amap Path Planning API Script

Plans routes between locations using different transportation modes.

Usage:
    # Address to address
    python scripts/path_planning.py --origin "北京市" --destination "上海市" --mode driving

    # Coordinate to coordinate
    python scripts/path_planning.py --origin "116.481485,39.990464" --destination "121.473701,31.230416" --mode driving

    # Address to coordinate
    python scripts/path_planning.py --origin "北京市" --destination "121.473701,31.230416" --mode driving
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
    parse_coordinates,
    geocode
)


MODES = {
    'driving': '/direction/driving',
    'walking': '/direction/walking',
    'cycling': '/direction/bicycling',
    'transit': '/direction/transit/integrated',
    'ebicycle': '/direction/ebicycling'
}


MODE_NAMES = {
    'driving': 'Driving',
    'walking': 'Walking',
    'cycling': 'Cycling',
    'transit': 'Transit'
}


def resolve_location(location: str, api_key: str) -> str:
    """
    Resolve location to coordinates if it's an address.

    Args:
        location: Location string (address or "lon,lat")
        api_key: Amap API key

    Returns:
        Coordinate string "lon,lat"
    """
    coords = parse_coordinates(location)
    if coords:
        return f"{coords[0]},{coords[1]}"

    # Geocode the address
    try:
        result = geocode(location, api_key=api_key)
        return result['location']
    except Exception as e:
        raise ValueError(f"Failed to resolve location '{location}': {e}")


def plan_route(origin: str, destination: str, mode: str, api_key: Optional[str] = None) -> dict:
    """
    Plan route between two locations.

    Args:
        origin: Start location (address or "lon,lat")
        destination: End location (address or "lon,lat")
        mode: Transportation mode: driving, walking, cycling, transit
        api_key: Amap API key (if None, will prompt)

    Returns:
        Route planning result dict
    """
    if mode not in MODES:
        raise ValueError(f"Invalid mode '{mode}'. Must be one of: {', '.join(MODES.keys())}")

    if api_key is None:
        api_key = get_api_key()

    # Resolve locations to coordinates
    origin_coords = resolve_location(origin, api_key)
    dest_coords = resolve_location(destination, api_key)

    params = {
        'origin': origin_coords,
        'destination': dest_coords
    }

    # Add mode-specific parameters
    if mode == 'transit':
        params['city'] = '全国'  # Can be overridden
        params['cityd'] = '全国'

    url = build_api_url(MODES[mode], params)
    data = make_api_request(url, api_key)

    if mode == 'transit':
        route = data.get('route', {})
        if not route.get('transits'):
            raise ValueError("No route found")
    else:
        route = data.get('route', {})
        if not route.get('paths'):
            raise ValueError("No route found")

    return route


def format_driving_result(result: dict) -> str:
    """Format driving/cycling/walking route result for display."""
    paths = result.get('paths', [])
    if not paths:
        return "No route found"

    path = paths[0]  # Get first route option

    distance = int(path.get('distance', 0))
    duration = int(path.get('duration', 0))
    tolls = int(path.get('tolls', 0))
    toll_distance = int(path.get('toll_distance', 0))

    steps = path.get('steps', [])

    output = []
    output.append(f"Route Summary:")
    output.append(f"  Distance: {distance}m ({distance/1000:.2f}km)")
    output.append(f"  Duration: {duration}s ({duration//60}m {duration%60}s)")
    if tolls > 0:
        output.append(f"  Tolls: {tolls}")
    if toll_distance > 0:
        output.append(f"  Toll Road Distance: {toll_distance}m")

    output.append(f"\nTurn-by-turn Directions ({len(steps)} steps):")
    for i, step in enumerate(steps, 1):
        instruction = step.get('instruction', '')
        step_distance = int(step.get('distance', 0))
        step_duration = int(step.get('duration', 0))
        output.append(f"\n{i}. {instruction}")
        output.append(f"   Distance: {step_distance}m, Duration: {step_duration}s")

    return '\n'.join(output)


def format_transit_result(result: dict) -> str:
    """Format transit route result for display."""
    transits = result.get('transits', [])
    if not transits:
        return "No route found"

    transit = transits[0]  # Get first route option

    distance = int(transit.get('distance', 0))
    duration = int(transit.get('duration', 0))
    cost = float(transit.get('cost', 0))

    segments = transit.get('segments', [])

    output = []
    output.append(f"Transit Route Summary:")
    output.append(f"  Distance: {distance}m ({distance/1000:.2f}km)")
    output.append(f"  Duration: {duration}s ({duration//60}m {duration%60}s)")
    output.append(f"  Cost: ¥{cost:.2f}")

    output.append(f"\nDetailed Itinerary ({len(segments)} segments):")
    for i, segment in enumerate(segments, 1):
        bus = segment.get('bus', {})
        walking = segment.get('walking', {})

        if bus.get('buslines'):
            busline = bus['buslines'][0]
            name = busline.get('name', '')
            departure = busline.get('departure_stop', {}).get('name', '')
            arrival = busline.get('arrival_stop', {}).get('name', '')
            via_num = busline.get('via_num', 0)
            output.append(f"\n{i}. {name}")
            output.append(f"   {departure} → {arrival}")
            output.append(f"   Stops: {via_num}")

        if walking.get('steps'):
            walk_distance = int(walking.get('distance', 0))
            walk_duration = int(walking.get('duration', 0))
            output.append(f"\n{i}. Walking")
            output.append(f"   Distance: {walk_distance}m, Duration: {walk_duration}s")

    return '\n'.join(output)


def format_route_result(result: dict, mode: str) -> str:
    """Format route result based on mode."""
    if mode == 'transit':
        return format_transit_result(result)
    else:
        return format_driving_result(result)


def main():
    parser = argparse.ArgumentParser(
        description='Amap Path Planning - Plan routes between locations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Address to address (driving)
  python scripts/path_planning.py --origin "北京市" --destination "上海市" --mode driving

  # Address to address (walking)
  python scripts/path_planning.py --origin "北京市天安门" --destination "北京市王府井" --mode walking

  # Coordinate to coordinate
  python scripts/path_planning.py --origin "116.481485,39.990464" --destination "121.473701,31.230416" --mode driving

  # Address to coordinate
  python scripts/path_planning.py --origin "北京市" --destination "121.473701,31.230416" --mode driving

Available modes:
  driving   - Driving route
  walking   - Walking route
  cycling   - Cycling route
  ebicycle  - E-bicycle route
  transit   - Public transit (bus, subway, etc.)
        """
    )

    parser.add_argument('--origin', type=str, required=True,
                        help='Start location (address or "longitude,latitude")')
    parser.add_argument('--destination', type=str, required=True,
                        help='End location (address or "longitude,latitude")')
    parser.add_argument('--mode', type=str, required=True, choices=list(MODES.keys()),
                        help='Transportation mode')

    args = parser.parse_args()

    try:
        result = plan_route(args.origin, args.destination, args.mode)
        print(f"\n{MODE_NAMES[args.mode]} Route Result:")
        print("=" * 50)
        print(format_route_result(result, args.mode))

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
