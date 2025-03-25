# ORFS Implementation Guide

## Getting Started with ORFS

This guide provides step-by-step instructions for implementing the Open Restaurant Feed Specification (ORFS) in your systems.

## Prerequisites

- Basic understanding of JSON and/or Protocol Buffers
- Ability to generate data exports from your restaurant management system
- Development environment with Python 3.6+ (for using the validation tools)

## Implementation Steps

### 1. Data Mapping

Map your existing data to ORFS concepts:

| Your System | ORFS Entity |
|-------------|-------------|
| Restaurant/Venue | `Restaurant` |
| Menu/Food List | `Menu` |
| Menu Item | `Dish` |
| Seating/Table | `Table` |
| Component/Ingredient | `Ingredient` |

### 2. Static Feed Implementation

1. Export your restaurant data as JSON following the ORFS schema
2. Include all required fields (marked as `required` in the protobuf definition)
3. Validate your feed using the ORFS validator tool
4. Host the JSON file on a web server or provide it via an API endpoint

Example implementation steps:

```python
import json
from datetime import datetime

# Create your ORFS data structure
orfs_feed = {
    "header": {
        "version": "1.0",
        "timestamp": int(datetime.now().timestamp()),
        "provider": "Your Restaurant Name"
    },
    "restaurants": [
        {
            "id": "your-restaurant-id",
            "name": "Your Restaurant Name",
            "description": "Your restaurant description",
            "location": {
                "latitude": 37.7749,
                "longitude": -122.4194,
                "address": "123 Your Street, Your City, YC 12345"
            },
            # Add menus, dishes, tables, etc.
        }
    ]
}

# Export to JSON file
with open("your_restaurant_feed.json", "w") as f:
    json.dump(orfs_feed, f, indent=2)
```

### 3. Real-time Feed Implementation

1. Install the Protocol Buffers compiler (`protoc`)
2. Generate language-specific code from the ORFS protobuf definition
3. Create real-time update messages for table status, dish availability, etc.
4. Publish these messages through a streaming API or websocket connection

Example of generating Python code from the protobuf definition:

```bash
protoc --python_out=. proto/orfs.proto
```

Example of creating a real-time update:

```python
import orfs_pb2
import time

# Create a feed message
feed = orfs_pb2.FeedMessage()

# Set header information
feed.header.version = "1.0"
feed.header.timestamp = int(time.time())
feed.header.provider = "Your Restaurant Name"
feed.header.incrementality = orfs_pb2.FeedHeader.DIFFERENTIAL

# Add an entity for a table update
entity = feed.entity.add()
entity.id = "your-restaurant-table-1"

# Set table information
entity.table.restaurant_id = "your-restaurant-id"
entity.table.table_id = "table-1"
entity.table.status = orfs_pb2.Table.AVAILABLE
entity.table.last_updated = int(time.time())

# Serialize the message
binary_data = feed.SerializeToString()
# Send this data through your chosen transport mechanism
```

### 4. Testing and Validation

1. Use the ORFS validator tool to check your feeds:
   ```bash
   python tools/validator.py --static path/to/your_feed.json
   ```

2. Use the sample consumer to verify how applications will read your data:
   ```bash
   python tools/sample_consumer.py --static path/to/your_feed.json
   ```

3. Check common issues:
   - Missing required fields
   - Incorrect data types
   - Invalid references between entities
   - Timestamp formatting issues

### 5. Publishing Your Feed

Options for making your ORFS feed available:

1. **Static File Hosting**:
   - Host your JSON file on a web server
   - Update it on a regular schedule (daily, hourly)
   - Provide an ETag or Last-Modified header for caching

2. **API Endpoint**:
   - Create a REST API that returns ORFS-formatted data
   - Include appropriate authentication if needed
   - Document the API for developers

3. **Real-time Stream**:
   - Use WebSockets, SSE, or message queues for real-time updates
   - Provide documentation on how to connect to your stream
   - Consider implementing reconnection handling

### 6. Best Practices

- Keep your feed size manageable (consider pagination for large datasets)
- Update static feeds at regular intervals
- Only send real-time updates when data actually changes
- Include proper versioning information
- Document any extensions you add to the standard
- Maintain consistent IDs across updates

## Resources

- [ORFS Specification](technical_reference.md)
- [Validation Tools](/tools)
- [Example Feeds](/examples)
