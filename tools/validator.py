#!/usr/bin/env python3
"""
ORFS Validator

This tool validates ORFS static feed JSON files against the JSON schema
and ORFS Protocol Buffer messages against the .proto definitions.

Usage:
  python validator.py --static path/to/static_feed.json
  python validator.py --realtime path/to/realtime_feed.json
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("Error: jsonschema package is required. Install with: pip install jsonschema")
    sys.exit(1)

try:
    import google.protobuf
except ImportError:
    print("Error: protobuf package is required. Install with: pip install protobuf")
    sys.exit(1)


def validate_static_feed(json_file_path):
    """Validate a static ORFS JSON feed against the schema."""
    # Load the schema
    schema_path = Path(__file__).parent.parent / "best-practices" / "orfs-schema.json"
    try:
        with open(schema_path, "r") as schema_file:
            schema = json.load(schema_file)
    except FileNotFoundError:
        print(f"Error: Schema file not found at {schema_path}")
        return False
    
    # Load the feed file
    try:
        with open(json_file_path, "r") as feed_file:
            feed = json.load(feed_file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: Could not load feed file: {e}")
        return False
    
    # Validate
    try:
        jsonschema.validate(instance=feed, schema=schema)
        print(f"✅ Static feed at {json_file_path} is valid!")
        return True
    except jsonschema.exceptions.ValidationError as e:
        print(f"❌ Validation error: {e}")
        return False


def validate_realtime_feed(proto_file_path):
    """Validate a realtime ORFS Protocol Buffer feed."""
    # In a real implementation, this would use the compiled protobuf
    # definitions to parse and validate the feed
    print("Realtime feed validation not yet implemented")
    return False


def main():
    parser = argparse.ArgumentParser(description='Validate ORFS feeds')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--static', help='Path to static JSON feed file to validate')
    group.add_argument('--realtime', help='Path to realtime Protocol Buffer feed file to validate')
    
    args = parser.parse_args()
    
    if args.static:
        success = validate_static_feed(args.static)
    elif args.realtime:
        success = validate_realtime_feed(args.realtime)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
