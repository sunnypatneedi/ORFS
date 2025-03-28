# ORFS Implementation Guide

## Getting Started with ORFS

This guide provides step-by-step instructions for implementing the Open Restaurant Feed Specification (ORFS) in your systems. It covers both the core ORFS v1.0 functionality and the enhanced marketing and narrative capabilities introduced in ORFS v1.1.

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
| Item Groupings | `Bundle` (v1.1) |
| Chef Stories | Narrative fields (v1.1) |
| Marketing Campaigns | `MarketingExtension` (v1.1) |
| Supplier Info | `SupplierLocation` (v1.1) |

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
        "version": "1.1",  # Update to latest version
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
            # Add v1.1 marketing extensions if available
            "key_message_points": [
                "Farm-to-table freshness",
                "Supporting local farmers"
            ],
            "marketing_extension": {
                "loyalty_program": {
                    "program_name": "Rewards Club",
                    "tiers": [
                        {
                            "tier_name": "Bronze",
                            "benefits": "5% off your bill"
                        }
                    ]
                }
            }
            # Add menus, dishes, tables, etc.
        }
    ],
    # Add other top-level arrays as needed
    "dishes": [],
    "ingredients": [],
    "bundles": []
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
feed.header.version = "1.1"  # Update to latest version
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

### 4. Implementing ORFS v1.1 Marketing Extensions

The v1.1 version of ORFS introduces powerful marketing capabilities that can significantly enhance your feed:

#### Adding Narrative Content

1. **Identify Narrative Sources**: Work with your chefs, suppliers, and marketing team to gather authentic stories
2. **Create TranslatedString Content**: Use the TranslatedString format for multi-language support

```python
# Example of creating chef story in multiple languages
chef_story = {
    "translations": {
        "en": "Chef Maria developed this recipe during her travels through Tuscany...",
        "es": "La chef María desarrolló esta receta durante sus viajes por la Toscana..."
    }
}

# Add to your dish data
dish_data = {
    "id": "margherita-pizza",
    "name": "Margherita Pizza",
    # Other standard fields...
    
    # Add narrative fields
    "chef_story": chef_story,
    "seasonal_story": {
        "translations": {
            "en": "Summer brings the most vibrant tomatoes..."
        }
    },
    "ingredient_story": {
        "translations": {
            "en": "Our tomatoes are sourced from Green Valley Farms..."
        }
    }
}
```

#### Implementing Supplier Location Data

```python
supplier_location = {
    "detailed": {
        "street_address": "123 Farm Road",
        "locality": "Green Valley",
        "state": "CA",
        "country": "USA",
        "zipcode": "95476"
    },
    "compact": "Green Valley, CA",
    "latitude": 38.291859,
    "longitude": -122.458036
}

# Add to your ingredient or dish data
ingredient_data = {
    "id": "tomatoes-organic",
    "name": "Organic Heirloom Tomatoes",
    # Other standard fields...
    
    "supplier_name": "Green Valley Farms",
    "supplier_location": supplier_location,
    "supplier_certification": "USDA Organic",
    "farm_distance": 15  # Distance in miles/km
}
```

#### Creating Marketing Extensions

```python
marketing_extension = {
    "loyalty_program": {
        "program_name": "Rewards Club",
        "tiers": [
            {
                "tier_name": "Bronze",
                "benefits": "5% off your bill"
            },
            {
                "tier_name": "Silver",
                "benefits": "10% off your bill + free dessert"
            }
        ],
        "promo_blurb": "Join our Rewards Club for exclusive benefits!"
    },
    "promotional_offers": [
        {
            "offer_name": "Happy Hour",
            "details": "Half-price appetizers, Monday-Friday, 4-6pm",
            "start_time": 1700000000,  # Unix timestamp
            "end_time": 1700007200,    # Unix timestamp
            "marketing_copy": "Start your evening right with our legendary happy hour!"
        }
    ],
    "social_media_strategy": {
        "platforms": ["Instagram", "Facebook"],
        "hashtags": ["#LocalFood", "#FarmToTable"],
        "posting_schedule": "2x weekly",
        "social_media_blurb": "Experience the best local ingredients, prepared with passion."
    }
}

# Add to your restaurant data
restaurant_data = {
    "id": "your-restaurant-id",
    "name": "Your Restaurant Name",
    # Other standard fields...
    
    "marketing_extension": marketing_extension,
    "key_message_points": [
        "Farm-to-table freshness",
        "Supporting local farmers",
        "Sustainable practices"
    ],
    "suggested_prompt_template": "Generate a {length} description for {restaurant_name}, emphasizing our {key_message_points}"
}
```

#### Defining Bundles

```python
bundle = {
    "id": "date-night-special",
    "restaurant_id": "your-restaurant-id",
    "bundle_name": "Date Night Special",
    "included_items": ["margherita-pizza", "tiramisu", "chianti-glass"],
    "price": 4500,  # In smallest currency unit (e.g., cents)
    "currency": "USD",
    "bundle_marketing_copy": "Enjoy a perfect evening with our signature pizza, homemade dessert, and a glass of fine wine."
}

# Add to your bundles array
orfs_feed["bundles"].append(bundle)
```

### 5. Testing and Validation

1. Use the ORFS validator tool to check your feeds:
   ```bash
   # Basic validation against schema
   python tools/validator.py --static path/to/your_feed.json
   
   # Enhanced marketing fields validation for v1.1
   python tools/validator.py --marketing-check path/to/your_feed.json
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
   - Language codes in TranslatedString (must be ISO 639-1 format)
   - Latitude/longitude ranges in SupplierLocation
   - Start time after end time in promotional offers
   - Missing translations in narrative fields

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

#### General Best Practices
- Keep your feed size manageable (consider pagination for large datasets)
- Update static feeds at regular intervals
- Only send real-time updates when data actually changes
- Include proper versioning information
- Document any extensions you add to the standard
- Maintain consistent IDs across updates

#### ORFS v1.1 Marketing Best Practices
- **Authenticity**: Ensure narrative content is authentic and truthful
- **Permission**: Get explicit permission from suppliers before including their details
- **Incremental Adoption**: Start with a few key narrative fields and expand over time
- **Translations**: Begin with your most important languages and dishes
- **Updates**: Keep marketing and promotional information current
- **Validation**: Use the enhanced marketing validator regularly
- **Content Quality**: Review narrative content for spelling, grammar, and brand voice
- **LLM Integration**: Follow the [LLM Integration Guide](llm_integration_guide.md) for AI content generation
- **Marketing Team Involvement**: See the [Marketing Guide](marketing_guide.md) for strategies

#### Real-time Marketing Updates
When implementing real-time marketing updates in ORFS v1.1:
- Only send updates for fields that have actually changed
- Use the `DIFFERENTIAL` incrementality type for efficient updates
- Consider update frequency limits to avoid overwhelming consumers
- Include complete entity context for narrative field updates

```python
# Example real-time update for a limited-time dish story
entity = feed.entity.add()
entity.id = "seasonal-dish-update"
entity.dish.id = "pumpkin-ravioli"
entity.dish.restaurant_id = "your-restaurant-id"
entity.dish.seasonal_story.translations["en"] = "Just in for the next two weeks - our chef's special fall harvest ravioli made with local pumpkins picked yesterday!"
```

## Resources

- [ORFS Specification](technical_reference.md)
- [Validation Tools](/tools)
- [Example Feeds](/examples)
- [LLM Integration Guide](llm_integration_guide.md)
- [Marketing Guide](marketing_guide.md)
- [v1.1 Static Feed Example](/examples/v1.1_static_feed.json)
- [v1.1 Real-time Feed Example](/examples/v1.1_realtime_feed.json)
