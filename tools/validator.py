#!/usr/bin/env python3
"""
ORFS Validator

This tool validates ORFS static feed JSON files against the JSON schema
and ORFS Protocol Buffer messages against the .proto definitions.

Supports both ORFS v1.0 and v1.1 with enhanced validation for marketing fields.

Usage:
  python validator.py --static path/to/static_feed.json
  python validator.py --realtime path/to/realtime_feed.json
  python validator.py --marketing-check path/to/feed.json
  python validator.py --marketing-check path/to/feed.json --content-quality
  python validator.py --marketing-check path/to/feed.json --seo-check
  python validator.py --marketing-check path/to/feed.json --all-checks
"""

import argparse
import json
import os
import sys
import re
import logging
import statistics
import string
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional, Set
from collections import Counter

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


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def load_json_file(file_path: str) -> Optional[Dict]:
    """Load and parse a JSON file."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Could not load file {file_path}: {e}")
        return None


def validate_static_feed(json_file_path: str) -> bool:
    """Validate a static ORFS JSON feed against the schema."""
    # Load the schema
    schema_path = Path(__file__).parent.parent / "best-practices" / "orfs-schema.json"
    schema = load_json_file(schema_path)
    if schema is None:
        return False
    
    # Load the feed file
    feed = load_json_file(json_file_path)
    if feed is None:
        return False
    
    # Check ORFS version
    version = feed.get("header", {}).get("version", "1.0")
    logging.info(f"Detected ORFS version: {version}")
    
    # Validate against schema
    try:
        jsonschema.validate(instance=feed, schema=schema)
        print(f"✅ Static feed at {json_file_path} is valid according to JSON schema!")
        return True
    except jsonschema.exceptions.ValidationError as e:
        print(f"❌ Schema validation error: {e}")
        return False


def validate_realtime_feed(proto_file_path: str) -> bool:
    """Validate a realtime ORFS Protocol Buffer feed."""
    # Check if it's actually a JSON file (some realtime feeds might be in JSON format)
    if proto_file_path.endswith('.json'):
        feed = load_json_file(proto_file_path)
        if feed is None:
            return False
        
        # Basic structure checks
        if "header" not in feed or "entity" not in feed:
            logging.error("Realtime feed missing required 'header' or 'entity' fields")
            return False
        
        # Check ORFS version
        version = feed.get("header", {}).get("version", "1.0")
        logging.info(f"Detected ORFS version: {version}")
        
        # Check incrementality field
        incrementality = feed.get("header", {}).get("incrementality")
        if incrementality not in ["FULL_DATASET", "DIFFERENTIAL"]:
            logging.error(f"Invalid incrementality value: {incrementality}")
            return False
        
        print(f"✅ Realtime feed (JSON format) at {proto_file_path} has valid structure!")
        return True
    else:
        # For actual Protocol Buffer files
        try:
            # This would use the compiled protobuf definitions to parse and validate
            logging.warning("Full Protocol Buffer validation not implemented yet")
            logging.info("Performing basic file checks only")
            
            # Check if file exists and is not empty
            if not os.path.exists(proto_file_path):
                logging.error(f"File not found: {proto_file_path}")
                return False
            
            if os.path.getsize(proto_file_path) == 0:
                logging.error(f"File is empty: {proto_file_path}")
                return False
            
            print(f"✅ Realtime feed at {proto_file_path} exists and is not empty.")
            print("Note: Full Protocol Buffer validation is not implemented.")
            return True
        except Exception as e:
            logging.error(f"Error validating Protocol Buffer file: {e}")
            return False


def validate_marketing_fields(json_file_path: str, content_quality: bool = False, seo_check: bool = False) -> bool:
    """Perform extended validation on ORFS v1.1 marketing fields."""
    feed = load_json_file(json_file_path)
    if feed is None:
        return False
    
    # Check ORFS version
    version = feed.get("header", {}).get("version", "1.0")
    if version != "1.1":
        logging.warning(f"Marketing fields validation is designed for ORFS v1.1, detected version: {version}")
    
    validation_issues = []
    
    # Check restaurant marketing extensions
    if "restaurants" in feed:
        for i, restaurant in enumerate(feed["restaurants"]):
            restaurant_id = restaurant.get("id", f"restaurant-{i}")
            
            # Check key_message_points
            if "key_message_points" in restaurant:
                points = restaurant["key_message_points"]
                if not points or not isinstance(points, list):
                    validation_issues.append(
                        f"Restaurant '{restaurant_id}' has empty or invalid key_message_points")
                elif content_quality:
                    # Check if key messages are effective (3-7 words is ideal for a key message)
                    for j, point in enumerate(points):
                        words = point.split()
                        if len(words) < 3:
                            validation_issues.append(
                                f"Restaurant '{restaurant_id}' key_message_point[{j}] is too short ({len(words)} words). Aim for 3-7 words.")
                        elif len(words) > 10:
                            validation_issues.append(
                                f"Restaurant '{restaurant_id}' key_message_point[{j}] is too long ({len(words)} words). Aim for 3-7 words.")
            
            # Check suggested_prompt_template
            if "suggested_prompt_template" in restaurant:
                template = restaurant["suggested_prompt_template"]
                if not template or not isinstance(template, str):
                    validation_issues.append(
                        f"Restaurant '{restaurant_id}' has empty or invalid suggested_prompt_template")
                else:
                    variables = ["restaurant_name", "key_message_points", "length"]
                    for var in variables:
                        if '{' + var + '}' not in template:
                            validation_issues.append(
                                f"Restaurant '{restaurant_id}' suggested_prompt_template should include {{{var}}}")
            
            # Check marketing_extension
            if "marketing_extension" in restaurant:
                marketing = restaurant["marketing_extension"]
                
                # Validate loyalty program
                if "loyalty_program" in marketing:
                    program = marketing["loyalty_program"]
                    if "tiers" in program and (not program["tiers"] or not isinstance(program["tiers"], list)):
                        validation_issues.append(
                            f"Restaurant '{restaurant_id}' has invalid loyalty program tiers")
                    
                    # Content quality checks for promo_blurb
                    if content_quality and "promo_blurb" in program:
                        blurb = program["promo_blurb"]
                        if len(blurb.split()) < 5:
                            validation_issues.append(
                                f"Restaurant '{restaurant_id}' loyalty program promo_blurb is too short. Aim for at least 5 words.")
                
                # Validate promotional offers
                if "promotional_offers" in marketing:
                    offers = marketing["promotional_offers"]
                    if not isinstance(offers, list):
                        validation_issues.append(
                            f"Restaurant '{restaurant_id}' promotional_offers must be a list")
                    else:
                        for j, offer in enumerate(offers):
                            # Check if timestamps make sense (end time after start time)
                            if "start_time" in offer and "end_time" in offer:
                                if offer["start_time"] > offer["end_time"]:
                                    validation_issues.append(
                                        f"Promotional offer '{offer.get('offer_name', 'unnamed')}' has end_time before start_time")
                            
                            # Content quality checks for marketing_copy
                            if content_quality and "marketing_copy" in offer:
                                copy = offer["marketing_copy"]
                                if len(copy.split()) < 5:
                                    validation_issues.append(
                                        f"Restaurant '{restaurant_id}' promotional_offer[{j}] marketing_copy is too short. Aim for at least 5 words.")
                                if not any(p in copy for p in "!?"):
                                    validation_issues.append(
                                        f"Restaurant '{restaurant_id}' promotional_offer[{j}] marketing_copy may be more engaging with exclamation or question marks.")
                
                # Validate social media strategy
                if "social_media_strategy" in marketing:
                    social = marketing["social_media_strategy"]
                    
                    # Check for required fields
                    for field in ["platforms", "hashtags"]:
                        if field not in social or not isinstance(social[field], list) or not social[field]:
                            validation_issues.append(
                                f"Restaurant '{restaurant_id}' social_media_strategy must include non-empty {field} list")
                    
                    # Content quality checks for social_media_blurb
                    if content_quality and "social_media_blurb" in social:
                        blurb = social["social_media_blurb"]
                        words = blurb.split()
                        if len(words) < 10:
                            validation_issues.append(
                                f"Restaurant '{restaurant_id}' social_media_blurb is too short ({len(words)} words). Aim for at least 10 words.")
                        
                        # Check hashtags format
                        if "hashtags" in social:
                            for hashtag in social["hashtags"]:
                                if not hashtag.startswith("#"):
                                    validation_issues.append(
                                        f"Restaurant '{restaurant_id}' hashtag '{hashtag}' should start with #")
                
                # Check call to action fields
                if "website_cta" in marketing:
                    cta = marketing["website_cta"]
                    if "button_text" in cta and len(cta["button_text"]) < 2:
                        validation_issues.append(
                            f"Restaurant '{restaurant_id}' website_cta button_text is too short")
                    if "target_url" in cta and not cta["target_url"].startswith("http"):
                        validation_issues.append(
                            f"Restaurant '{restaurant_id}' website_cta target_url should start with http:// or https://")
    
    # Check dish narrative fields
    if "dishes" in feed:
        for dish in feed["dishes"]:
            dish_id = dish.get("id", "unknown")
            dish_name = dish.get("name", dish_id)
            
            # Check for translated strings
            narrative_fields = ["chef_story", "chef_highlight", "chef_anecdote", "culinary_philosophy", 
                               "seasonal_story", "cultural_context", "ingredient_story"]
            
            for field in narrative_fields:
                if field in dish:
                    translated = dish[field]
                    if not isinstance(translated, dict) or "translations" not in translated:
                        validation_issues.append(
                            f"Dish '{dish_id}' has invalid {field} format - must use TranslatedString format")
                    elif "translations" in translated:
                        translations = translated["translations"]
                        if not translations or not isinstance(translations, dict):
                            validation_issues.append(
                                f"Dish '{dish_id}' has empty or invalid translations in {field}")
                        else:
                            for lang_code, content in translations.items():
                                # Check language code format
                                if not re.match(r'^[a-z]{2}$', lang_code):
                                    validation_issues.append(
                                        f"Dish '{dish_id}' has invalid language code '{lang_code}' in {field}")
                                
                                # Content quality checks if enabled
                                if content_quality:
                                    words = content.split()
                                    # Check content length
                                    if field == "chef_highlight" and len(words) > 50:
                                        validation_issues.append(
                                            f"Dish '{dish_id}' {field} is too long ({len(words)} words). Aim for under 50 words.")
                                    elif field == "chef_highlight" and len(words) < 10:
                                        validation_issues.append(
                                            f"Dish '{dish_id}' {field} is too short ({len(words)} words). Aim for at least 10 words.")
                                    elif field in ["chef_story", "seasonal_story", "cultural_context"] and len(words) < 30:
                                        validation_issues.append(
                                            f"Dish '{dish_id}' {field} is too short ({len(words)} words). Aim for at least 30 words.")
                                    
                                    # Check punctuation and readability
                                    if len(content) > 0 and content[-1] not in [".", "!", "?"]:
                                        validation_issues.append(
                                            f"Dish '{dish_id}' {field} should end with proper punctuation.")
                                    
                                    # Check for dish name inclusion
                                    if dish_name.lower() not in content.lower() and len(words) > 20:
                                        validation_issues.append(
                                            f"Dish '{dish_id}' {field} should mention the dish name '{dish_name}' for better SEO.")
                                    
                                    # Check for text quality metrics
                                    if len(words) > 15:
                                        # Average word length (too high might indicate overly complex language)
                                        avg_word_len = sum(len(word) for word in words) / len(words)
                                        if avg_word_len > 8:
                                            validation_issues.append(
                                                f"Dish '{dish_id}' {field} has high average word length ({avg_word_len:.1f}). Consider simplifying language.")
                                        
                                        # Check for sentence variety
                                        sentences = re.split(r'[.!?]+', content)
                                        sentences = [s.strip() for s in sentences if s.strip()]
                                        if len(sentences) > 1:
                                            sent_lengths = [len(s.split()) for s in sentences]
                                            if max(sent_lengths) == min(sent_lengths):
                                                validation_issues.append(
                                                    f"Dish '{dish_id}' {field} has uniform sentence lengths. Consider varying sentence structure.")
            
            # Check supplier information and sustainability impact
            if "supplier_location" in dish:
                location = dish["supplier_location"]
                # Check coordinate ranges
                if "latitude" in location and (location["latitude"] < -90 or location["latitude"] > 90):
                    validation_issues.append(
                        f"Dish '{dish_id}' has invalid latitude in supplier_location: {location['latitude']}")
                if "longitude" in location and (location["longitude"] < -180 or location["longitude"] > 180):
                    validation_issues.append(
                        f"Dish '{dish_id}' has invalid longitude in supplier_location: {location['longitude']}")
                
                # Check for completeness
                if "detailed" in location:
                    detailed = location["detailed"]
                    required_fields = ["street_address", "locality", "state", "country"]
                    missing = [f for f in required_fields if f not in detailed or not detailed[f]]
                    if missing:
                        validation_issues.append(
                            f"Dish '{dish_id}' supplier_location.detailed is missing: {', '.join(missing)}")
            
            if "supplier_certification" in dish and len(dish["supplier_certification"]) < 2:
                validation_issues.append(
                    f"Dish '{dish_id}' has invalid supplier_certification: too short")
            
            if "farm_distance" in dish:
                distance = dish["farm_distance"]
                if not isinstance(distance, (int, float)) or distance <= 0:
                    validation_issues.append(
                        f"Dish '{dish_id}' has invalid farm_distance: {distance}. Must be a positive number.")
                elif distance > 500:
                    validation_issues.append(
                        f"Warning: Dish '{dish_id}' has a large farm_distance: {distance}. Verify if this is correct.")
            
            if "sustainability_impact" in dish:
                impact = dish["sustainability_impact"]
                if not isinstance(impact, str) or len(impact) < 10:
                    validation_issues.append(
                        f"Dish '{dish_id}' has invalid sustainability_impact: too short. Aim for at least 10 words.")
            
            # Check upgrade options (now an array in v1.2)
            if "upgrade_options" in dish:
                options = dish["upgrade_options"]
                if not isinstance(options, list):
                    validation_issues.append(
                        f"Dish '{dish_id}' upgrade_options must be an array")
                else:
                    for i, option in enumerate(options):
                        if not isinstance(option, dict):
                            validation_issues.append(
                                f"Dish '{dish_id}' upgrade_options[{i}] must be an object")
                            continue
                            
                        if "new_name" not in option or not option["new_name"]:
                            validation_issues.append(
                                f"Dish '{dish_id}' upgrade_options[{i}] is missing new_name")
                                
                        if "new_price" in option and not isinstance(option["new_price"], (int, float)):
                            validation_issues.append(
                                f"Dish '{dish_id}' upgrade_options[{i}] has invalid new_price")
                                
                        if "marketing_copy" not in option or not option["marketing_copy"]:
                            validation_issues.append(
                                f"Dish '{dish_id}' upgrade_options[{i}] is missing marketing_copy")
            
            # Check LTO details (new in v1.2)
            if "lto_details" in dish:
                lto = dish["lto_details"]
                if not isinstance(lto, dict):
                    validation_issues.append(
                        f"Dish '{dish_id}' lto_details must be an object")
                else:
                    # Validate required fields
                    if "start_time" not in lto or not isinstance(lto["start_time"], (int)):
                        validation_issues.append(
                            f"Dish '{dish_id}' lto_details is missing valid start_time")
                            
                    if "end_time" not in lto or not isinstance(lto["end_time"], (int)):
                        validation_issues.append(
                            f"Dish '{dish_id}' lto_details is missing valid end_time")
                    
                    # Check that end_time is after start_time
                    if "start_time" in lto and "end_time" in lto and lto["start_time"] >= lto["end_time"]:
                        validation_issues.append(
                            f"Dish '{dish_id}' lto_details has end_time that is not after start_time")
                    
                    if "marketing_copy" not in lto or not isinstance(lto["marketing_copy"], str) or len(lto["marketing_copy"]) < 10:
                        validation_issues.append(
                            f"Dish '{dish_id}' lto_details is missing or has too short marketing_copy")
            
            # Check customer feedback summary (new in v1.2)
            if "customer_feedback_summary" in dish:
                feedback = dish["customer_feedback_summary"]
                if not isinstance(feedback, str) or len(feedback) < 5:
                    validation_issues.append(
                        f"Dish '{dish_id}' has invalid customer_feedback_summary: too short")
    
    # Check bundle fields
    if "bundles" in feed:
        for bundle in feed["bundles"]:
            bundle_id = bundle.get("bundle_id", "unknown")
            
            # Check bundle name
            if "bundle_name" not in bundle or not bundle["bundle_name"]:
                validation_issues.append(f"Bundle '{bundle_id}' must have a bundle_name")
            
            # Check included_items
            if "included_items" not in bundle or not bundle["included_items"]:
                validation_issues.append(f"Bundle '{bundle_id}' must have at least one item in included_items")
            
            # Check bundle price
            if "bundle_price" not in bundle or not isinstance(bundle["bundle_price"], (int, float)) or bundle["bundle_price"] <= 0:
                validation_issues.append(f"Bundle '{bundle_id}' must have a valid bundle_price greater than zero")
            
            # Check marketing copy
            if "bundle_marketing_copy" in bundle and (not isinstance(bundle["bundle_marketing_copy"], str) or len(bundle["bundle_marketing_copy"]) < 10):
                validation_issues.append(f"Bundle '{bundle_id}' has invalid or too short bundle_marketing_copy")
    
    # Check for SEO best practices if requested
    if seo_check and ("restaurants" in feed or "dishes" in feed):
        # Collect all narrative content for SEO analysis
        all_marketing_text = []
        keywords = set()
        
        # Extract restaurant marketing texts
        if "restaurants" in feed:
            for restaurant in feed["restaurants"]:
                restaurant_id = restaurant.get("id", "unknown")
                restaurant_name = restaurant.get("name", restaurant_id)
                
                # Add key message points to keywords
                if "key_message_points" in restaurant:
                    keywords.update([point.lower() for point in restaurant["key_message_points"]])
                
                # Add marketing extension texts
                if "marketing_extension" in restaurant:
                    marketing = restaurant["marketing_extension"]
                    
                    if "loyalty_program" in marketing and "promo_blurb" in marketing["loyalty_program"]:
                        all_marketing_text.append(marketing["loyalty_program"]["promo_blurb"])
                    
                    if "promotional_offers" in marketing:
                        for offer in marketing["promotional_offers"]:
                            if "marketing_copy" in offer:
                                all_marketing_text.append(offer["marketing_copy"])
                    
                    if "social_media_strategy" in marketing and "social_media_blurb" in marketing["social_media_strategy"]:
                        all_marketing_text.append(marketing["social_media_strategy"]["social_media_blurb"])
        
        # Extract dish narrative texts
        if "dishes" in feed:
            for dish in feed["dishes"]:
                dish_name = dish.get("name", dish.get("id", "unknown"))
                keywords.add(dish_name.lower())
                
                # Add narrative fields
                narrative_fields = ["chef_story", "chef_highlight", "seasonal_story", "cultural_context", "ingredient_story"]
                for field in narrative_fields:
                    if field in dish and "translations" in dish[field]:
                        for lang, text in dish[field]["translations"].items():
                            all_marketing_text.append(text)
        
        # Perform SEO analysis
        if all_marketing_text:
            # Get unique words excluding common stopwords (simplified list)
            stopwords = {"a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for", "is", "are", "was", "were"}
            all_words = []
            for text in all_marketing_text:
                words = [word.lower().strip(string.punctuation) for word in text.split()]
                all_words.extend([w for w in words if w and w not in stopwords])
            
            # Get word frequencies
            word_count = Counter(all_words)
            most_common = word_count.most_common(10)
            
            # Check if keywords are being used consistently
            keyword_usage = {k: word_count.get(k.strip(string.punctuation), 0) for k in keywords if k.strip(string.punctuation)}
            unused_keywords = [k for k, count in keyword_usage.items() if count == 0]
            low_use_keywords = [k for k, count in keyword_usage.items() if 0 < count < 3 and len(all_marketing_text) > 5]
            
            # Add SEO recommendations
            if unused_keywords:
                validation_issues.append(
                    f"SEO: Some key terms are not used in marketing text: {', '.join(unused_keywords)}")
            
            if low_use_keywords:
                validation_issues.append(
                    f"SEO: Some key terms have low usage in marketing text: {', '.join(low_use_keywords)}")
            
            # Print SEO analysis
            print(f"\nSEO Analysis:")
            print(f"  Total marketing texts analyzed: {len(all_marketing_text)}")
            print(f"  Most frequent words used: {', '.join([f'{word} ({count})' for word, count in most_common])}")
            print(f"  Key term usage: {', '.join([f'{k} ({v})' for k, v in keyword_usage.items() if v > 0])}")
    
    # Report validation results
    if validation_issues:
        print(f"\n❌ Found {len(validation_issues)} issues with marketing fields:")
        for issue in validation_issues:
            print(f"  - {issue}")
        return False
    else:
        print(f"\n✅ Marketing fields in {json_file_path} pass enhanced validation checks!")
        return True


def main():
    parser = argparse.ArgumentParser(description='Validate ORFS feeds')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--static', help='Path to static JSON feed file to validate')
    group.add_argument('--realtime', help='Path to realtime Protocol Buffer or JSON feed file to validate')
    group.add_argument('--marketing-check', help='Perform enhanced validation on marketing fields in v1.1 feeds')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    parser.add_argument('--content-quality', action='store_true', help='Enable enhanced content quality checks for marketing narrative')
    parser.add_argument('--seo-check', action='store_true', help='Enable SEO optimization checks for marketing content')
    parser.add_argument('--all-checks', action='store_true', help='Enable all enhanced validation checks')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    if args.static:
        success = validate_static_feed(args.static)
    elif args.realtime:
        success = validate_realtime_feed(args.realtime)
    elif args.marketing_check:
        # Set content quality and SEO check flags
        content_quality = args.content_quality or args.all_checks
        seo_check = args.seo_check or args.all_checks
        
        success = validate_marketing_fields(
            args.marketing_check, 
            content_quality=content_quality,
            seo_check=seo_check
        )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
