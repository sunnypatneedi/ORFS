# ORFS Technical Reference

## Data Model

### FeedMessage

The root message for both static and real-time ORFS feeds.

```protobuf
message FeedMessage {
  required FeedHeader header = 1;
  repeated FeedEntity entity = 2;
}
```

### FeedHeader

Contains metadata about the feed.

```protobuf
message FeedHeader {
  required string version = 1;
  required uint64 timestamp = 2;
  optional string provider = 3;
  optional Incrementality incrementality = 4;
}
```

### Restaurant

Represents a restaurant establishment.

```protobuf
message Restaurant {
  required string id = 1;
  required string name = 2;
  optional string description = 3;
  required Location location = 4;
  optional Contact contact = 5;
  repeated Hours hours = 6;
  repeated string cuisine_type = 7;
  optional string price_range = 8;
  optional bool accepts_reservations = 9;
  repeated Menu menus = 10;
  repeated Table tables = 11;
}
```

### Menu

Represents a collection of dishes available at specific times.

```protobuf
message Menu {
  required string id = 1;
  required string name = 2;
  optional string description = 3;
  repeated TimeRange active_times = 4;
  repeated Dish dishes = 5;
}
```

### Dish

Represents a food or beverage item with pricing and customization options.

```protobuf
message Dish {
  required string id = 1;
  required string name = 2;
  optional string description = 3;
  required Price price = 4;
  repeated Ingredient ingredients = 5;
  repeated DishCustomization customizations = 6;
  optional NutritionalInfo nutritional_info = 7;
  optional string image_url = 8;
  optional bool available = 9;
  optional DishCategory category = 10;
}
```

## Extensions

ORFS supports extensions to allow vendor-specific additions:

- Field numbers 1000-1999 are reserved for public extensions
- Field numbers 9000-9999 are reserved for private extensions

## Validation Rules

### Restaurant ID

- Must be unique within a feed
- Must be alphanumeric with hyphens or underscores only
- Pattern: `^[A-Za-z0-9_-]+$`

### Coordinates

- Latitude must be between -90 and 90
- Longitude must be between -180 and 180

### Time Values

- Must follow ISO 8601 format for times (HH:MM:SS)
- Must specify timezone for absolute times

### Prices

- Currency codes must follow ISO 4217 format (3 uppercase letters)
- Amount must be positive

## Protocol Buffer and JSON Conversion

When converting between Protocol Buffer and JSON representations:

1. Field names use `snake_case` in both formats
2. Enums use UPPERCASE values in both formats
3. Timestamps are represented as integers (seconds since epoch) in both formats

## Data Integrity

1. All ID references must reference valid entities within the feed
2. Required fields must always be present
3. Enumerated values must match one of the defined values

See [validation tools](/tools/validator.py) for automated compliance checking.
