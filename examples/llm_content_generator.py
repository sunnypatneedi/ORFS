#!/usr/bin/env python3
"""
ORFS LLM Content Generator Example

This script demonstrates how to use the ORFS v1.1 marketing extensions
to automatically generate engaging content using Large Language Models.

It requires an LLM API key (OpenAI by default, but configurable for other providers).

Usage:
  python llm_content_generator.py --input path/to/feed.json --output path/to/output.json
  python llm_content_generator.py --dish-id dish123 --input path/to/feed.json
  python llm_content_generator.py --restaurant-id rest123 --input path/to/feed.json
"""

import argparse
import json
import os
import sys
import logging
import requests
import time
from typing import Dict, List, Any, Optional, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# OpenAI API configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
DEFAULT_MODEL = "gpt-3.5-turbo"  # Can be configured to other models

# LLM provider options
SUPPORTED_PROVIDERS = ["openai", "anthropic", "local"]


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


def call_openai_api(prompt: str, model: str = DEFAULT_MODEL) -> Optional[str]:
    """Call the OpenAI API with a prompt and return the generated text."""
    if not OPENAI_API_KEY:
        logging.error("OpenAI API key not found. Set the OPENAI_API_KEY environment variable.")
        return None

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a skilled food writer and marketer helping create engaging content for restaurants."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(OPENAI_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"].strip()
        else:
            logging.error(f"Unexpected API response structure: {result}")
            return None
    except Exception as e:
        logging.error(f"Error calling OpenAI API: {e}")
        return None


def call_llm_api(prompt: str, provider: str = "openai", model: str = DEFAULT_MODEL) -> Optional[str]:
    """Call an LLM API based on the provider and return the generated text."""
    if provider == "openai":
        return call_openai_api(prompt, model)
    elif provider == "anthropic":
        # Integration with Anthropic Claude would go here
        logging.error("Anthropic API not yet implemented. Please use 'openai' provider.")
        return None
    elif provider == "local":
        # Example of a mock local LLM for testing without API keys
        logging.warning("Using local mock LLM (for testing only)")
        return f"[LOCAL LLM MOCK] Generated content based on: {prompt[:50]}..."
    else:
        logging.error(f"Unsupported LLM provider: {provider}")
        return None


def generate_dish_narrative(dish: Dict, field: str, provider: str = "openai", model: str = DEFAULT_MODEL) -> Optional[Dict]:
    """Generate narrative content for a specified dish field using LLM."""
    dish_name = dish.get("name", "")
    dish_description = dish.get("description", "")
    
    if not dish_name:
        logging.error("Dish must have a name for narrative generation")
        return None
    
    # Define field-specific prompts if no template is available
    default_prompts = {
        "chef_story": f"Write a compelling chef's story (100-150 words) for the dish '{dish_name}'. Include details about the inspiration, culinary journey, and passion behind creating this dish.",
        
        "chef_highlight": f"Write a brief highlight (30-50 words) about the chef's special connection to the dish '{dish_name}'.",
        
        "seasonal_story": f"Write a seasonal story (100-150 words) for the dish '{dish_name}', explaining how it connects to the current season, ingredients availability, and traditions.",
        
        "cultural_context": f"Write about the cultural context (100-150 words) of the dish '{dish_name}'. Include its origins, significance in its culture, and how it has evolved.",
        
        "ingredient_story": f"Write a story (100-150 words) about the key ingredients in the dish '{dish_name}'. Focus on sourcing, quality, and what makes these ingredients special."
    }
    
    # Check if the field exists and we have a template for it
    if field not in default_prompts and (field not in dish or "suggested_prompt_template" not in dish):
        logging.error(f"No template available for field '{field}'")
        return None
    
    # Use the dish's suggested prompt template if available
    if "suggested_prompt_template" in dish:
        prompt_template = dish["suggested_prompt_template"]
        # Gather variables for the template
        template_vars = {
            "dish_name": dish_name,
            "length": "150 words",
            "key_ingredient": "its key ingredients"  # Default value
        }
        
        # Extract key_ingredient from description if possible
        if dish_description and "with" in dish_description:
            ingredients_part = dish_description.split("with", 1)[1].strip()
            template_vars["key_ingredient"] = ingredients_part
        
        prompt = prompt_template.format(**template_vars)
    else:
        # Fall back to default prompts
        prompt = default_prompts.get(field, f"Write content for {field} field for the dish '{dish_name}'.")
    
    # Call the LLM API
    generated_text = call_llm_api(prompt, provider, model)
    
    if not generated_text:
        return None
    
    # Create TranslatedString structure
    return {
        "translations": {
            "en": generated_text
        }
    }


def generate_restaurant_content(restaurant: Dict, field: str, provider: str = "openai", model: str = DEFAULT_MODEL) -> Optional[str]:
    """Generate marketing content for a restaurant field using LLM."""
    restaurant_name = restaurant.get("name", "")
    
    if not restaurant_name:
        logging.error("Restaurant must have a name for content generation")
        return None
    
    # Get key message points if available
    key_message_points = restaurant.get("key_message_points", [])
    key_points_text = ", ".join(key_message_points) if key_message_points else "quality, authentic cuisine"
    
    # Define field-specific prompts
    default_prompts = {
        "description": f"Write an engaging description (100-150 words) for {restaurant_name}. Emphasize these key points: {key_points_text}.",
        
        "social_media_blurb": f"Write a catchy social media bio (50-60 words) for {restaurant_name} that would work on Instagram or Facebook. Emphasize: {key_points_text}.",
        
        "loyalty_program_promo": f"Write a promotional blurb (30-40 words) for {restaurant_name}'s loyalty program that encourages customers to sign up. Emphasize: {key_points_text}."
    }
    
    # Check if we have a template for this field
    if field not in default_prompts and "suggested_prompt_template" not in restaurant:
        logging.error(f"No template available for field '{field}'")
        return None
    
    # Use the restaurant's suggested prompt template if available
    if "suggested_prompt_template" in restaurant:
        prompt_template = restaurant["suggested_prompt_template"]
        # Gather variables for the template
        template_vars = {
            "restaurant_name": restaurant_name,
            "key_message_points": key_points_text,
            "length": "150 words"
        }
        
        prompt = prompt_template.format(**template_vars)
    else:
        # Fall back to default prompts
        prompt = default_prompts.get(field, f"Write content for {field} field for {restaurant_name}.")
    
    # Call the LLM API
    return call_llm_api(prompt, provider, model)


def update_dish_narratives(feed: Dict, dish_id: Optional[str] = None, provider: str = "openai", model: str = DEFAULT_MODEL) -> Dict:
    """Update narrative fields for one or all dishes in a feed using LLM."""
    if "dishes" not in feed:
        logging.error("No dishes found in feed")
        return feed
    
    updated_feed = feed.copy()
    
    # Fields to generate content for
    narrative_fields = ["chef_story", "seasonal_story", "cultural_context", "ingredient_story", "chef_highlight"]
    
    # Process each dish or just the specified one
    for i, dish in enumerate(updated_feed["dishes"]):
        current_dish_id = dish.get("id")
        
        # Skip if we're targeting a specific dish and this isn't it
        if dish_id and current_dish_id != dish_id:
            continue
        
        dish_name = dish.get("name", f"Dish {i+1}")
        logging.info(f"Generating narrative content for dish: {dish_name}")
        
        # Generate content for each narrative field
        for field in narrative_fields:
            # Skip if the field already has content
            if field in dish and dish[field].get("translations", {}).get("en"):
                logging.info(f"  Field '{field}' already has content, skipping...")
                continue
                
            logging.info(f"  Generating content for field: {field}")
            content = generate_dish_narrative(dish, field, provider, model)
            
            if content:
                dish[field] = content
                logging.info(f"  Content generated for {field}")
            else:
                logging.warning(f"  Failed to generate content for {field}")
            
            # Add a small delay to avoid rate limits
            time.sleep(1)
    
    return updated_feed


def update_restaurant_marketing(feed: Dict, restaurant_id: Optional[str] = None, provider: str = "openai", model: str = DEFAULT_MODEL) -> Dict:
    """Update marketing content for one or all restaurants in a feed using LLM."""
    if "restaurants" not in feed:
        logging.error("No restaurants found in feed")
        return feed
    
    updated_feed = feed.copy()
    
    # Process each restaurant or just the specified one
    for restaurant in updated_feed["restaurants"]:
        current_restaurant_id = restaurant.get("id")
        
        # Skip if we're targeting a specific restaurant and this isn't it
        if restaurant_id and current_restaurant_id != restaurant_id:
            continue
        
        restaurant_name = restaurant.get("name", "Restaurant")
        logging.info(f"Generating marketing content for restaurant: {restaurant_name}")
        
        # Update restaurant description if empty
        if not restaurant.get("description"):
            logging.info("  Generating restaurant description")
            description = generate_restaurant_content(restaurant, "description", provider, model)
            if description:
                restaurant["description"] = description
                logging.info("  Description generated")
            time.sleep(1)
        
        # Ensure marketing_extension exists
        if "marketing_extension" not in restaurant:
            restaurant["marketing_extension"] = {}
        
        marketing = restaurant["marketing_extension"]
        
        # Update social media strategy blurb
        if "social_media_strategy" not in marketing:
            marketing["social_media_strategy"] = {}
        
        social = marketing["social_media_strategy"]
        if not social.get("social_media_blurb"):
            logging.info("  Generating social media blurb")
            blurb = generate_restaurant_content(restaurant, "social_media_blurb", provider, model)
            if blurb:
                social["social_media_blurb"] = blurb
                
                # Add default platforms and hashtags if not present
                if "platforms" not in social:
                    social["platforms"] = ["Instagram", "Facebook"]
                
                if "hashtags" not in social:
                    social["hashtags"] = ["#LocalFood", "#FarmToTable"]
                
                logging.info("  Social media blurb generated")
            time.sleep(1)
        
        # Update loyalty program
        if "loyalty_program" not in marketing:
            marketing["loyalty_program"] = {
                "program_name": f"{restaurant_name} Rewards",
                "tiers": [
                    {
                        "tier_name": "Regular",
                        "benefits": "10% off your bill"
                    }
                ]
            }
        
        loyalty = marketing["loyalty_program"]
        if not loyalty.get("promo_blurb"):
            logging.info("  Generating loyalty program promo")
            promo = generate_restaurant_content(restaurant, "loyalty_program_promo", provider, model)
            if promo:
                loyalty["promo_blurb"] = promo
                logging.info("  Loyalty program promo generated")
            time.sleep(1)
    
    return updated_feed


def main():
    parser = argparse.ArgumentParser(description='ORFS LLM Content Generator Example')
    parser.add_argument('--input', required=True, help='Input ORFS feed JSON file')
    parser.add_argument('--output', help='Output file for the enhanced feed (defaults to input_enhanced.json)')
    parser.add_argument('--dish-id', help='ID of a specific dish to generate content for')
    parser.add_argument('--restaurant-id', help='ID of a specific restaurant to generate content for')
    parser.add_argument('--provider', choices=SUPPORTED_PROVIDERS, default="local", 
                        help='LLM provider to use (default: local - for testing without API)')
    parser.add_argument('--model', default=DEFAULT_MODEL, help='Model name for the LLM provider')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Check for API key if using a cloud provider
    if args.provider == "openai" and not OPENAI_API_KEY:
        logging.error("OpenAI API key not found. Set the OPENAI_API_KEY environment variable.")
        logging.info("For testing without an API key, use --provider=local")
        sys.exit(1)
    
    # Load the feed
    feed = load_json_file(args.input)
    if not feed:
        sys.exit(1)
    
    # Check if feed is ORFS v1.1
    version = feed.get("header", {}).get("version", "1.0")
    if version != "1.1":
        logging.warning(f"This script is designed for ORFS v1.1, detected version: {version}")
        
        # Update the version
        if "header" not in feed:
            feed["header"] = {}
        feed["header"]["version"] = "1.1"
    
    # Generate content
    if args.dish_id:
        logging.info(f"Generating narrative content for dish ID: {args.dish_id}")
        updated_feed = update_dish_narratives(feed, args.dish_id, args.provider, args.model)
    elif args.restaurant_id:
        logging.info(f"Generating marketing content for restaurant ID: {args.restaurant_id}")
        updated_feed = update_restaurant_marketing(feed, args.restaurant_id, args.provider, args.model)
    else:
        logging.info("Generating content for all restaurants and dishes")
        # First update restaurants, then dishes
        temp_feed = update_restaurant_marketing(feed, None, args.provider, args.model)
        updated_feed = update_dish_narratives(temp_feed, None, args.provider, args.model)
    
    # Save the output
    if args.output:
        output_file = args.output
    else:
        input_base = os.path.splitext(args.input)[0]
        output_file = f"{input_base}_enhanced.json"
    
    success = save_json_file(updated_feed, output_file)
    
    if success:
        logging.info(f"Enhanced feed saved to: {output_file}")
        if args.provider == "local":
            logging.info("Note: Content was generated with the local mock provider. For real content, use --provider=openai with an API key.")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
