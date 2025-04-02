# Open Restaurant Feed Specification (ORFS)
**Version:** 1.2  
**Last Updated:** 2025-03-28
![image](https://github.com/user-attachments/assets/a3aab2de-31af-4bc3-947a-2b3548ac6aac)

![image](https://github.com/user-attachments/assets/8e122b35-44f6-42de-9f2c-452917820194)


ORFS is an open, real-time protocol for restaurants to broadcast detailed information about their menus, dishes, tables, and ingredients. ORFS uses Protocol Buffers for efficient real-time feeds and JSON for static data interchange. Version 1.2 enhances the specification with multiple upgrade options, limited-time offers, customer feedback summaries, and improved LLM integration to generate more compelling content.

## Overview

This repository contains:
- **Protobuf Definitions:** Found in `proto/orfs.proto`
- **JSON Schemas:** In the `best-practices/` folder, providing full validation for Restaurant, Menu, Dish, Table, Ingredient, Bundle, and marketing extension types.
- **Examples:** Example static feed and real-time feed files in `examples/`, including v1.2 examples demonstrating the latest features.
- **Tools:** Reference implementations and a validator script in `tools/`.
- **Documentation:** Detailed markdown documentation in `spec/`.

## Key Features in v1.2

- **Rich Narrative Content:** Tell compelling stories about dishes, ingredients, and chef inspirations
- **Multi-language Support:** Provide translations for key narrative content
- **Marketing Extensions:** Include loyalty program details, promotional offers, events, and more
- **Local Sourcing Data:** Showcase farm locations, certifications, and sustainability impacts
- **Multiple Upgrade Options:** Offer several premium modifications for any dish (new in v1.2)
- **Limited-Time Offers:** Specify time-bound promotions with start/end times (new in v1.2)
- **Customer Feedback Summary:** Highlight customer favorites and review sentiment (new in v1.2)
- **Enhanced LLM Integration:** Improved prompt templates for better auto-generation of marketing content
- **Bundle Offerings:** Define and promote groups of items sold together
- **Backward Compatibility:** All new fields are optional to maintain compatibility with earlier versions

## Quick Start

1. **Generating Code from Protobuf:**

   ```bash
   # For example, to generate Python classes:
   protoc --python_out=. proto/orfs.proto
   ```

2. **Validating a JSON Feed:**

   Use the provided Python validator:

   ```bash
   python tools/validator.py examples/static_feed.json best-practices/restaurant.schema.json
   ```

3. **Running the Sample Consumer:**

   This sample consumer reads a real-time feed (protobuf or JSON) and prints updates.

   ```bash
   python tools/sample_consumer.py examples/realtime_feed.json
   ```

## Contributing

Please see the CONTRIBUTING.md file for full documentation, design rationale, and contribution guidelines.

## License

This project is licensed under the Apache License 2.0 – see the LICENSE file for details.
