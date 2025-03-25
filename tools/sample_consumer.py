#!/usr/bin/env python3
"""
ORFS Sample Consumer

This script demonstrates how to consume and process ORFS data feeds.
It can handle both static JSON feeds and real-time Protocol Buffer feeds.

Usage:
  python sample_consumer.py --static path/to/static_feed.json
  python sample_consumer.py --realtime path/to/realtime_feed.json
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# In a real implementation, this would import generated Protocol Buffer classes
# from the ORFS proto definitions
# from orfs_pb2 import FeedMessage


def process_static_feed(json_file_path):
    """Process a static ORFS JSON feed."""
    # Load the feed file
    try:
        with open(json_file_path, "r") as feed_file:
            feed = json.load(feed_file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: Could not load feed file: {e}")
        return False

    # Process header
    header = feed.get("header", {})
    version = header.get("version", "unknown")
    timestamp = header.get("timestamp", 0)
    timestamp_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    provider = header.get("provider", "unknown")
    
    print(f"ORFS Feed Version: {version}")
    print(f"Feed Timestamp: {timestamp_str}")
    print(f"Feed Provider: {provider}")
    
    # Process restaurants
    restaurants = feed.get("restaurants", [])
    print(f"\nFound {len(restaurants)} restaurants in feed:")
    
    for restaurant in restaurants:
        print(f"\n- {restaurant.get('name', 'Unnamed Restaurant')}")
        print(f"  ID: {restaurant.get('id', 'No ID')}")
        print(f"  Description: {restaurant.get('description', 'No description')}")
        
        # Location info
        location = restaurant.get("location", {})
        if location:
            print(f"  Address: {location.get('address', 'No address')}")
            print(f"  Coordinates: {location.get('latitude', 'N/A')}, {location.get('longitude', 'N/A')}")
        
        # Menu summary
        menus = restaurant.get("menus", [])
        print(f"  Menus: {len(menus)}")
        
        for menu in menus:
            print(f"    - {menu.get('name', 'Unnamed Menu')}")
            dishes = menu.get("dishes", [])
            print(f"      Dishes: {len(dishes)}")
            
            # Print first few dishes
            for i, dish in enumerate(dishes[:3]):
                price_info = dish.get("price", {})
                price_str = f"{price_info.get('amount', 'N/A')} {price_info.get('currency', '')}"
                print(f"        {dish.get('name', 'Unnamed Dish')} - {price_str}")
            
            if len(dishes) > 3:
                print(f"        ... and {len(dishes) - 3} more dishes")
        
        # Table summary
        tables = restaurant.get("tables", [])
        print(f"  Tables: {len(tables)}")
        
    return True


def process_realtime_feed(proto_file_path):
    """Process a realtime ORFS Protocol Buffer feed."""
    # In a real implementation, this would use the compiled protobuf
    # definitions to parse and process the feed
    print("Realtime feed processing not yet implemented")
    print("This would parse the Protocol Buffer message and display real-time updates")
    print("Such as table availability, wait times, and menu item availability")
    return False


def main():
    parser = argparse.ArgumentParser(description='Sample ORFS feed consumer')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--static', help='Path to static JSON feed file to process')
    group.add_argument('--realtime', help='Path to realtime Protocol Buffer feed file to process')
    
    args = parser.parse_args()
    
    if args.static:
        success = process_static_feed(args.static)
    elif args.realtime:
        success = process_realtime_feed(args.realtime)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
