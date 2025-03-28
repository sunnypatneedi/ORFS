# ORFS Change Log

All notable changes to the ORFS specification will be documented in this file.

## [1.1.0] - 2025-05-15

Major enhancement to the ORFS specification adding marketing, narrative, and local sourcing capabilities.

### Added
- New message types in Protocol Buffer definitions:
  - `TranslatedString` for multi-language text support
  - `SupplierLocation` for detailed and compact supplier address representation
  - `MarketingExtension` with fields for loyalty programs, promotions, events, and more
  - `UpgradeOption` for dish variants and upselling
  - `Bundle` for grouped item offerings
- Extended the Dish message with new marketing and narrative fields:
  - `chef_highlight`, `chef_story`, `chef_anecdote` for authentic chef narratives
  - `culinary_philosophy`, `seasonal_story`, `cultural_context` for rich storytelling
  - `ingredient_story` for detailed ingredient narratives
  - `supplier_location`, `supplier_certification`, `farm_distance` for local sourcing data
  - `sustainability_impact` for environmental messaging
  - `upgrade_options` for premium variations
  - `key_message_points` and `suggested_prompt_template` for LLM integration
- Enhanced Restaurant message with MarketingExtension and LLM guidance fields
- Updated JSON Schema with extensive validation for all new fields
- Added comprehensive examples of v1.1 static and real-time feeds
- All new fields are optional to maintain backward compatibility

### Changed
- Update validation rules to support new data types
- Expanded documentation with guidelines for marketing content
- Improved real-time feed structure for marketing updates

## [1.0.0-draft] - 2025-03-22

Initial draft of the ORFS specification.

### Added
- Core Protocol Buffer definitions for FeedMessage, Restaurant, Menu, Dish, Table, and Ingredient
- JSON Schema validation for all data types
- Example static and real-time feeds
- Basic validation and sample consumer tools
- Initial documentation structure
