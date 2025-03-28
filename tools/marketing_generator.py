#!/usr/bin/env python3
"""
ORFS Marketing Content Generator

This tool helps generate template content for ORFS v1.1 marketing and narrative fields.
It creates starter templates based on restaurant and dish information.

Usage:
  python marketing_generator.py --create-templates path/to/basic_feed.json --output path/to/output_dir
  python marketing_generator.py --enhance-field chef_story --input path/to/feed.json --dish-id dish123
  python marketing_generator.py --generate-bundle-promotion --input path/to/feed.json
"""

import argparse
import json
import os
import sys
import logging
import textwrap
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Template definitions for narrative fields
NARRATIVE_TEMPLATES = {
    "chef_highlight": "A {dish_adjective} {dish_name} prepared by Chef {chef_name}, featuring {key_ingredient}.",
    
    "chef_story": """
        During {chef_name}'s travels to {location}, {pronoun} discovered the inspiration for our {dish_name}.
        This dish combines traditional techniques with {chef_name}'s unique approach to {cuisine_type} cooking.
        Each {dish_name} is prepared with meticulous attention to detail, ensuring a memorable dining experience.
    """,
    
    "chef_anecdote": """
        Chef {chef_name} recalls: "The first time I made {dish_name} was during {event}. 
        I was struck by how the {key_ingredient} created such a profound flavor when combined with {secondary_ingredient}. 
        It's become one of my favorite dishes to prepare for our guests."
    """,
    
    "culinary_philosophy": """
        At {restaurant_name}, we believe that exceptional food starts with exceptional ingredients.
        Our {dish_name} embodies our philosophy of {philosophy_point}.
        We're committed to {commitment_point} while delivering unforgettable flavors in every dish.
    """,
    
    "seasonal_story": """
        {season_name} brings the perfect conditions for our {dish_name}.
        The {key_ingredient} reaches its peak during this time, harvested from {farm_name} just {farm_distance} miles away.
        We prepare this seasonal favorite using traditional {method} techniques to highlight its natural {quality}.
    """,
    
    "cultural_context": """
        The {dish_name} has deep roots in {culture} cuisine, where it has been enjoyed for generations.
        Traditionally served during {occasion}, this dish represents {cultural_significance}.
        Our version honors these traditions while adding subtle contemporary elements.
    """,
    
    "ingredient_story": """
        Our {key_ingredient} comes directly from {supplier_name} in {supplier_location}.
        The {supplier_name} family has been growing {key_ingredient} for {years} years using {farming_method}.
        Their commitment to {certification} practices ensures that our {dish_name} features only the finest ingredients.
    """
}

# Template for marketing extensions
MARKETING_EXTENSION_TEMPLATE = {
    "loyalty_program": {
        "program_name": "{restaurant_name} Rewards",
        "tiers": [
            {
                "tier_name": "Silver",
                "benefits": "10% off your bill"
            },
            {
                "tier_name": "Gold",
                "benefits": "15% off your bill + complimentary dessert"
            },
            {
                "tier_name": "Platinum",
                "benefits": "20% off your bill + priority reservations + chef's surprise"
            }
        ],
        "promo_blurb": "Join our {restaurant_name} Rewards program and enjoy exclusive benefits every time you dine with us!"
    },
    "promotional_offers": [
        {
            "offer_name": "Happy Hour",
            "details": "Half-price appetizers and drink specials, Monday-Friday, 4-6pm",
            "start_time": 0,  # Will be filled with current time
            "end_time": 0,    # Will be filled with current time + 30 days
            "marketing_copy": "Unwind after work with friends and enjoy our legendary Happy Hour specials!"
        },
        {
            "offer_name": "Date Night Special",
            "details": "Three-course dinner for two with a bottle of house wine, $99",
            "start_time": 0,  # Will be filled with current time
            "end_time": 0,    # Will be filled with current time + 30 days
            "marketing_copy": "Make it a night to remember with our romantic Date Night Special!"
        }
    ],
    "social_media_strategy": {
        "platforms": ["Instagram", "Facebook", "Twitter"],
        "hashtags": ["#{restaurant_name_no_spaces}", "#LocalFood", "#FarmToTable"],
        "posting_schedule": "3x weekly",
        "social_media_blurb": "Follow us on social media for behind-the-scenes looks at our kitchen, chef specials, and exclusive offers only available to our followers!"
    },
    "website_cta": {
        "button_text": "Reserve Now",
        "target_url": "https://www.{restaurant_domain}/reservations",
        "cta_copy": "Secure your table today for an unforgettable dining experience!"
    }
}

# Bundle template
BUNDLE_TEMPLATE = {
    "id": "{restaurant_id}_{bundle_name}",
    "restaurant_id": "{restaurant_id}",
    "bundle_name": "{bundle_name}",
    "included_items": [],  # Will be filled dynamically
    "price": 0,  # Will be calculated
    "currency": "USD",
    "bundle_marketing_copy": "Experience the best of {restaurant_name} with our {bundle_name}. A perfect combination of our chef's favorite creations at a special price!"
}


def load_json_file(file_path: str) -> Optional[Dict]:
    """Load and parse a JSON file."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Could not load file {file_path}: {e}")
        return None


def save_json_file(data: Dict, file_path: str) -> bool:
    """Save data to a JSON file."""
    try:
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        
        logging.info(f"Successfully saved to {file_path}")
        return True
    except Exception as e:
        logging.error(f"Failed to save to {file_path}: {e}")
        return False


def clean_format_string(text: str) -> str:
    """Clean and format multi-line template strings."""
    lines = text.split('\n')
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    return ' '.join(cleaned_lines)


def create_translated_string(text: str, languages: List[str] = ["en"]) -> Dict:
    """Create a TranslatedString object with the given text in specified languages."""
    translations = {}
    for lang in languages:
        translations[lang] = text
    
    return {
        "translations": translations
    }


def generate_dish_templates(dish: Dict, restaurant: Dict) -> Dict:
    """Generate narrative templates for a dish."""
    dish_name = dish.get("name", "Signature Dish")
    restaurant_name = restaurant.get("name", "Our Restaurant")
    
    # Placeholder values for template variables
    template_vars = {
        "dish_name": dish_name,
        "dish_adjective": "exquisite",
        "restaurant_name": restaurant_name,
        "chef_name": "Alex",
        "pronoun": "they",
        "key_ingredient": "locally-sourced ingredients",
        "secondary_ingredient": "seasonal herbs",
        "location": "Southern France",
        "cuisine_type": "Mediterranean",
        "event": "a summer festival",
        "philosophy_point": "respecting ingredients and traditions",
        "commitment_point": "sustainability and supporting local farmers",
        "season_name": "Summer",
        "farm_name": "Green Valley Farm",
        "farm_distance": "15",
        "method": "slow-cooking",
        "quality": "freshness",
        "culture": "Mediterranean",
        "occasion": "harvest celebrations",
        "cultural_significance": "community and sharing",
        "supplier_name": "Green Valley Farm",
        "supplier_location": "the local countryside",
        "years": "three generations",
        "farming_method": "traditional organic",
        "certification": "sustainable"
    }
    
    # Generate templates for each narrative field
    narrative_fields = {}
    for field, template in NARRATIVE_TEMPLATES.items():
        # Clean up the template and format with placeholders
        cleaned_template = clean_format_string(template)
        formatted_text = cleaned_template.format(**template_vars)
        
        # Create TranslatedString
        narrative_fields[field] = create_translated_string(formatted_text)
    
    # Add supplier location
    narrative_fields["supplier_location"] = {
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
    
    # Add other marketing fields
    narrative_fields["supplier_certification"] = "USDA Organic"
    narrative_fields["farm_distance"] = 15
    narrative_fields["sustainability_impact"] = "Reduces carbon footprint by using local ingredients and sustainable farming practices."
    
    # Add upgrade options
    narrative_fields["upgrade_options"] = [
        {
            "name": "Premium ingredients",
            "description": "Upgrade to premium organic ingredients",
            "price_adjustment": 500
        },
        {
            "name": "Extra portion",
            "description": "50% larger portion",
            "price_adjustment": 700
        }
    ]
    
    # Add key message points
    narrative_fields["key_message_points"] = [
        "Farm-to-table freshness",
        "Chef's signature creation",
        "Seasonal ingredients"
    ]
    
    # Add LLM prompt template
    narrative_fields["suggested_prompt_template"] = "Generate a {length} description for {dish_name}, highlighting the use of {key_ingredient} and its {quality}."
    
    return narrative_fields


def generate_restaurant_marketing(restaurant: Dict) -> Dict:
    """Generate marketing extension template for a restaurant."""
    restaurant_name = restaurant.get("name", "Our Restaurant")
    restaurant_id = restaurant.get("id", "restaurant123")
    
    # Clean restaurant name for hashtags and domains
    restaurant_name_no_spaces = restaurant_name.replace(" ", "")
    restaurant_domain = restaurant_name_no_spaces.lower() + ".com"
    
    # Current time and future time for promotions
    current_time = int(datetime.now().timestamp())
    future_time = int((datetime.now() + timedelta(days=30)).timestamp())
    
    # Template variables
    template_vars = {
        "restaurant_name": restaurant_name,
        "restaurant_name_no_spaces": restaurant_name_no_spaces,
        "restaurant_domain": restaurant_domain,
        "restaurant_id": restaurant_id
    }
    
    # Clone the template
    marketing = json.loads(json.dumps(MARKETING_EXTENSION_TEMPLATE))
    
    # Format strings with template variables
    marketing["loyalty_program"]["program_name"] = marketing["loyalty_program"]["program_name"].format(**template_vars)
    marketing["loyalty_program"]["promo_blurb"] = marketing["loyalty_program"]["promo_blurb"].format(**template_vars)
    
    # Set promotion times
    for offer in marketing["promotional_offers"]:
        offer["start_time"] = current_time
        offer["end_time"] = future_time
    
    # Format social media
    new_hashtags = []
    for hashtag in marketing["social_media_strategy"]["hashtags"]:
        new_hashtags.append(hashtag.format(**template_vars))
    marketing["social_media_strategy"]["hashtags"] = new_hashtags
    
    # Format CTA
    marketing["website_cta"]["target_url"] = marketing["website_cta"]["target_url"].format(**template_vars)
    
    # Add key message points to restaurant
    key_message_points = [
        "Farm-to-table dining experience",
        "Supporting local farmers",
        "Sustainable practices",
        "Seasonal menu changes"
    ]
    
    # Add suggested prompt template
    suggested_prompt_template = "Generate a {length} description for {restaurant_name}, emphasizing our {key_message_points}"
    
    return {
        "marketing_extension": marketing,
        "key_message_points": key_message_points,
        "suggested_prompt_template": suggested_prompt_template
    }


def generate_bundle(feed: Dict, restaurant_id: str, bundle_name: str) -> Dict:
    """Generate a bundle of dishes for a restaurant."""
    # Find restaurant and its dishes
    restaurant = None
    restaurant_dishes = []
    
    if "restaurants" in feed:
        for rest in feed["restaurants"]:
            if rest.get("id") == restaurant_id:
                restaurant = rest
                break
    
    if not restaurant:
        logging.error(f"Restaurant with ID {restaurant_id} not found")
        return None
    
    # Find dishes for this restaurant
    if "dishes" in feed:
        for dish in feed["dishes"]:
            if dish.get("restaurant_id") == restaurant_id:
                restaurant_dishes.append(dish)
    
    if not restaurant_dishes:
        logging.error(f"No dishes found for restaurant {restaurant_id}")
        return None
    
    # Select up to 3 dishes for the bundle (appetizer, main, dessert if possible)
    selected_dishes = []
    dish_types = ["appetizer", "main", "dessert"]
    
    # Try to find one dish of each type
    for dish_type in dish_types:
        for dish in restaurant_dishes:
            category = dish.get("category", "").lower()
            if dish_type in category and dish not in selected_dishes:
                selected_dishes.append(dish)
                break
    
    # If we couldn't find enough dishes by category, just add more
    while len(selected_dishes) < min(3, len(restaurant_dishes)):
        for dish in restaurant_dishes:
            if dish not in selected_dishes:
                selected_dishes.append(dish)
                break
    
    # Calculate bundle price (with discount)
    total_price = sum(dish.get("price", 0) for dish in selected_dishes)
    discounted_price = int(total_price * 0.85)  # 15% bundle discount
    
    # Create bundle template
    template_vars = {
        "restaurant_id": restaurant_id,
        "bundle_name": bundle_name,
        "restaurant_name": restaurant.get("name", "Our Restaurant")
    }
    
    bundle = json.loads(json.dumps(BUNDLE_TEMPLATE))
    
    # Format bundle fields
    bundle["id"] = bundle["id"].format(**template_vars)
    bundle["restaurant_id"] = restaurant_id
    bundle["bundle_name"] = bundle_name
    bundle["included_items"] = [dish.get("id") for dish in selected_dishes]
    bundle["price"] = discounted_price
    bundle["bundle_marketing_copy"] = bundle["bundle_marketing_copy"].format(**template_vars)
    
    return bundle


def create_marketing_templates(input_file: str, output_dir: str) -> bool:
    """Create marketing templates based on a feed file."""
    feed = load_json_file(input_file)
    if not feed:
        return False
    
    # Check ORFS version
    version = feed.get("header", {}).get("version", "1.0")
    if version != "1.1":
        logging.warning(f"This tool is designed for ORFS v1.1, detected version: {version}")
        logging.info("Will create a v1.1 feed with marketing extensions")
    
    # Create output feed (copy of input with marketing fields added)
    output_feed = feed.copy()
    output_feed["header"]["version"] = "1.1"
    
    # Update restaurants with marketing extensions
    if "restaurants" in output_feed:
        for i, restaurant in enumerate(output_feed["restaurants"]):
            restaurant_id = restaurant.get("id", f"restaurant-{i}")
            logging.info(f"Generating marketing templates for restaurant: {restaurant.get('name', restaurant_id)}")
            
            # Generate marketing extension
            marketing_fields = generate_restaurant_marketing(restaurant)
            
            # Update restaurant with marketing fields
            restaurant.update(marketing_fields)
    
    # Update dishes with narrative fields
    if "dishes" in output_feed and "restaurants" in output_feed:
        for i, dish in enumerate(output_feed["dishes"]):
            dish_id = dish.get("id", f"dish-{i}")
            restaurant_id = dish.get("restaurant_id")
            
            # Find the associated restaurant
            restaurant = None
            for rest in output_feed["restaurants"]:
                if rest.get("id") == restaurant_id:
                    restaurant = rest
                    break
            
            if not restaurant:
                logging.warning(f"Restaurant not found for dish {dish_id}, using default values")
                restaurant = {"name": "Our Restaurant"}
            
            logging.info(f"Generating narrative templates for dish: {dish.get('name', dish_id)}")
            
            # Generate narrative fields
            narrative_fields = generate_dish_templates(dish, restaurant)
            
            # Update dish with narrative fields
            dish.update(narrative_fields)
    
    # Add bundles if not present
    if "bundles" not in output_feed:
        output_feed["bundles"] = []
    
    # Generate a bundle for each restaurant
    if "restaurants" in output_feed:
        for restaurant in output_feed["restaurants"]:
            restaurant_id = restaurant.get("id")
            restaurant_name = restaurant.get("name", "Our Restaurant")
            
            # Create bundle names
            bundle_names = ["Chef's Selection", "Family Feast", "Date Night Special"]
            
            for bundle_name in bundle_names:
                logging.info(f"Generating bundle '{bundle_name}' for restaurant: {restaurant_name}")
                bundle = generate_bundle(output_feed, restaurant_id, bundle_name)
                if bundle:
                    output_feed["bundles"].append(bundle)
    
    # Save the output feed
    output_file = os.path.join(output_dir, "marketing_enhanced_feed.json")
    return save_json_file(output_feed, output_file)


def enhance_narrative_field(input_file: str, dish_id: str, field_name: str) -> bool:
    """Enhance a specific narrative field for a dish."""
    feed = load_json_file(input_file)
    if not feed:
        return False
    
    # Find the dish
    dish = None
    if "dishes" in feed:
        for d in feed["dishes"]:
            if d.get("id") == dish_id:
                dish = d
                break
    
    if not dish:
        logging.error(f"Dish with ID {dish_id} not found")
        return False
    
    # Find the restaurant
    restaurant = None
    restaurant_id = dish.get("restaurant_id")
    if "restaurants" in feed and restaurant_id:
        for r in feed["restaurants"]:
            if r.get("id") == restaurant_id:
                restaurant = r
                break
    
    if not restaurant:
        logging.warning(f"Restaurant not found for dish {dish_id}, using default values")
        restaurant = {"name": "Our Restaurant"}
    
    # Generate narrative field templates
    narrative_fields = generate_dish_templates(dish, restaurant)
    
    if field_name in narrative_fields:
        # Update the specific field
        dish[field_name] = narrative_fields[field_name]
        logging.info(f"Enhanced {field_name} for dish {dish.get('name', dish_id)}")
        
        # Save the updated feed
        output_file = input_file.replace(".json", f"_enhanced_{field_name}.json")
        return save_json_file(feed, output_file)
    else:
        logging.error(f"Field {field_name} not found in narrative templates")
        return False


def generate_bundle_promotion(input_file: str) -> bool:
    """Generate a bundle promotion for each restaurant in the feed."""
    feed = load_json_file(input_file)
    if not feed:
        return False
    
    if "restaurants" not in feed:
        logging.error("No restaurants found in feed")
        return False
    
    # Create bundles if not present
    if "bundles" not in feed:
        feed["bundles"] = []
    
    for restaurant in feed["restaurants"]:
        restaurant_id = restaurant.get("id")
        restaurant_name = restaurant.get("name", "Our Restaurant")
        
        # Create a seasonal bundle
        current_month = datetime.now().strftime("%B")
        bundle_name = f"{current_month} Special"
        
        logging.info(f"Generating seasonal bundle '{bundle_name}' for {restaurant_name}")
        bundle = generate_bundle(feed, restaurant_id, bundle_name)
        
        if bundle:
            # Add seasonal marketing copy
            season_map = {
                "January": "winter", "February": "winter", "March": "spring",
                "April": "spring", "May": "spring", "June": "summer",
                "July": "summer", "August": "summer", "September": "fall",
                "October": "fall", "November": "fall", "December": "winter"
            }
            current_season = season_map.get(current_month, "seasonal")
            
            bundle["bundle_marketing_copy"] = (
                f"Celebrate {current_season} at {restaurant_name} with our {bundle_name}. "
                f"A carefully curated selection of {len(bundle['included_items'])} dishes "
                f"featuring the freshest {current_season} ingredients, available for a limited time."
            )
            
            feed["bundles"].append(bundle)
    
    # Save the updated feed
    output_file = input_file.replace(".json", f"_with_seasonal_bundles.json")
    return save_json_file(feed, output_file)


def main():
    parser = argparse.ArgumentParser(description='ORFS Marketing Content Generator')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--create-templates', help='Create marketing templates based on a basic feed file')
    group.add_argument('--enhance-field', help='Enhance a specific narrative field for a dish')
    group.add_argument('--generate-bundle-promotion', action='store_true', help='Generate a bundle promotion for each restaurant')
    
    parser.add_argument('--output', help='Output directory for generated files')
    parser.add_argument('--input', help='Input feed file')
    parser.add_argument('--dish-id', help='ID of the dish to enhance')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    if args.create_templates:
        if not args.output:
            logging.error("--output directory is required with --create-templates")
            sys.exit(1)
        
        success = create_marketing_templates(args.create_templates, args.output)
    
    elif args.enhance_field:
        if not args.input or not args.dish_id:
            logging.error("--input and --dish-id are required with --enhance-field")
            sys.exit(1)
        
        success = enhance_narrative_field(args.input, args.dish_id, args.enhance_field)
    
    elif args.generate_bundle_promotion:
        if not args.input:
            logging.error("--input is required with --generate-bundle-promotion")
            sys.exit(1)
        
        success = generate_bundle_promotion(args.input)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
