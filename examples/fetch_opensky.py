#!/usr/bin/env python3
"""
Fetch live aircraft snapshot from OpenSky Network.

Usage:
    python examples/fetch_opensky.py [--bbox EU|TR|GLOBAL]

Note:
    Anonymous OpenSky API has a rate limit of one request per 10
    seconds. Register an account for higher limits if needed.
"""

import argparse
import sys
try:
    import requests
except ImportError:
    print("Error: requests not installed. Run: pip install requests")
    sys.exit(1)

OPENSKY_URL = "https://opensky-network.org/api/states/all"

BBOXES = {
    "EU":     {"lamin": 35.0, "lamax": 71.0, "lomin": -10.0, "lomax":  40.0},
    "TR":     {"lamin": 35.0, "lamax": 43.0, "lomin":  25.0, "lomax":  45.0},
    "GLOBAL": {},
}

def fetch_states(bbox="EU"):
    params = BBOXES.get(bbox, {})
    print(f"Fetching OpenSky states for bbox={bbox}...")
    try:
        r = requests.get(OPENSKY_URL, params=params, timeout=15)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching OpenSky API: {e}")
        return None
    data = r.json()
    return data

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--bbox", default="EU", choices=list(BBOXES.keys()))
    args = p.parse_args()

    data = fetch_states(bbox=args.bbox)
    if data is None:
        sys.exit(1)
    states = data.get("states") or []
    print(f"Snapshot time: {data.get('time')}")
    print(f"Aircraft count: {len(states)}")
    print()
    print("First 5 aircraft:")
    print("-" * 70)
    for s in states[:5]:
        icao24, callsign, country, *_, lon, lat, alt = (s + [None]*15)[:8]
        print(f"  ICAO24={icao24}  callsign={callsign}  "
              f"country={country}  lat={lat}  lon={lon}")

if __name__ == "__main__":
    main()
