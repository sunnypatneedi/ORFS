# ORFS v1.1 LLM Integration Guide

## Introduction

This guide provides detailed instructions on how to leverage the marketing and narrative fields in ORFS v1.1 with Large Language Models (LLMs) to auto-generate engaging content for restaurants. The enhanced ORFS specification includes specific fields designed to facilitate seamless integration with LLMs, enabling restaurants to create compelling storytelling experiences around their dishes, ingredients, and overall brand.

## Key ORFS v1.1 Fields for LLM Integration

### Prompt Templates

ORFS v1.1 introduces `suggested_prompt_template` fields at both the restaurant and dish levels. These templates contain placeholders that can be dynamically filled with values from your ORFS feed:

```json
"suggested_prompt_template": "Generate a {length} description for {restaurant_name}, emphasizing our {key_message_points} and how we work with local suppliers within {farm_distance} miles of our restaurant."
```

Common placeholders include:
- `{length}` - Desired output length (e.g., "short", "150-word", "detailed")
- `{restaurant_name}` - Name of the restaurant
- `{dish.name}` - Name of a specific dish
- `{key_message_points}` - Core messaging priorities
- `{medium}` - Target medium (e.g., "menu", "social_media", "website")

### Key Message Points

The `key_message_points` arrays provide a list of core value statements or messaging priorities that should be emphasized in generated content:

```json
"key_message_points": [
  "Farm-to-table freshness",
  "Supporting local farmers",
  "Sustainable practices",
  "Celebrating California's bounty"
]
```

These points ensure generated content aligns with your restaurant's brand values and marketing strategy.

### Narrative Fields

ORFS v1.1 includes several narrative fields that provide rich context for LLMs:

- `chef_story` - The chef's inspiration or connection to a dish
- `ingredient_story` - Details about special ingredients and their origins
- `seasonal_story` - Context about seasonal relevance
- `cultural_context` - Historical or cultural significance
- `sustainability_impact` - Environmental benefits

These fields can be used as reference material for LLMs to generate more authentic and detailed content.

### Multi-language Support

The `TranslatedString` type allows for storing text in multiple languages:

```json
"chef_story": {
  "translations": {
    "en": "Inspired by her first visit to an Italian market...",
    "es": "Inspirada por su primera visita a un mercado italiano..."
  }
}
```

This enables LLMs to generate content in the appropriate language and adapt culturally relevant references.

## Implementation Strategies

### 1. Basic Content Generation

The simplest implementation strategy involves:

1. Extract data from your ORFS feed
2. Fill in the placeholders in the `suggested_prompt_template`
3. Send the completed prompt to an LLM API
4. Use the generated content in your application

Example implementation (Python with OpenAI):

```python
import openai
import json

# Load ORFS data
with open('orfs_feed.json', 'r') as f:
    orfs_data = json.load(f)

# Get restaurant data
restaurant = orfs_data['restaurants'][0]

# Fill prompt template with actual values
prompt_template = restaurant['suggested_prompt_template']
prompt = prompt_template.replace('{restaurant_name}', restaurant['name'])
prompt = prompt.replace('{length}', '150-word')
prompt = prompt.replace('{key_message_points}', ', '.join(restaurant['key_message_points']))
prompt = prompt.replace('{farm_distance}', '25')  # Example value

# Send to LLM API
response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    max_tokens=250,
    temperature=0.7
)

# Use the generated content
generated_description = response.choices[0].text.strip()
print(generated_description)
```

### 2. Context-Enhanced Generation

For more sophisticated outputs, provide the LLM with additional context from the narrative fields:

```python
# Gather additional context
context = f"""
Restaurant Description: {restaurant['description']}

Chef's Philosophy: {restaurant['culinary_philosophy']}

About our ingredients: {dish['ingredient_story']['translations']['en']}

Our sustainability impact: {dish['sustainability_impact']}
"""

# Enhance the prompt with context
enhanced_prompt = f"{context}\n\nBased on the information above, {prompt}"

# Send to LLM API
response = openai.Completion.create(
    model="text-davinci-003",
    prompt=enhanced_prompt,
    max_tokens=300,
    temperature=0.7
)
```

### 3. Dynamic Content Generation

For real-time applications like digital menus or websites, implement dynamic content generation:

1. Set up a backend service that processes ORFS feeds
2. Pre-generate common content during off-peak hours
3. Cache generated content with appropriate TTL values
4. Trigger real-time generation only for new or changed items

### 4. Multi-Channel Content Adaptation

Leverage the same ORFS data to generate content customized for different channels:

```python
# Generate social media post
social_prompt = dish['suggested_prompt_template'].replace('{medium}', 'social_media')
# ... complete and send to LLM

# Generate menu description
menu_prompt = dish['suggested_prompt_template'].replace('{medium}', 'menu')
# ... complete and send to LLM

# Generate website content
website_prompt = dish['suggested_prompt_template'].replace('{medium}', 'website')
# ... complete and send to LLM
```

## Best Practices

### Content Quality Assurance

1. **Human Review**: Always implement a human review process before publishing auto-generated content
2. **Content Guidelines**: Provide specific guidelines in your prompts (tone, style, length)
3. **Fact Checking**: Verify that generated content accurately reflects your restaurant's actual offerings
4. **Consistency**: Ensure generated content maintains brand voice across channels

### Technical Considerations

1. **Rate Limiting**: Implement appropriate rate limiting for LLM API calls
2. **Caching**: Cache generated content to reduce API costs and improve performance
3. **Fallbacks**: Have default content ready if LLM generation fails
4. **Versioning**: Track which version of content is being used where

### Security and Privacy

1. **Data Handling**: Be careful not to include sensitive information in LLM prompts
2. **Output Sanitization**: Validate and sanitize LLM outputs before displaying them
3. **Consent**: Ensure you have proper consent for using supplier/farm information in marketing

## Example Use Cases

### 1. Auto-generating Daily Specials Descriptions

```python
special_dish = get_daily_special_from_orfs()
prompt = f"Create an enticing 50-word description for today's special, {special_dish['name']}, highlighting its {special_dish['seasonal_story']} and {special_dish['chef_anecdote']}."
# Generate and display on digital menu boards
```

### 2. Creating Personalized Social Media Content

```python
# Use ORFS data to create targeted social posts
farm_story = dish['supplier_location']['compact'] + " " + dish['ingredient_story']
prompt = f"Write an Instagram post about our {dish['name']} featuring ingredients from {farm_story}. Include hashtags related to local sourcing and sustainability."
```

### 3. Generating Multi-lingual Menu Descriptions

```python
languages = ["en", "es", "fr", "zh"]
translations = {}

for lang in languages:
    prompt = f"Translate the following dish description to {lang}: {dish['description']}. Maintain the tone but adapt any cultural references appropriately."
    # Generate and store translations
```

## Conclusion

ORFS v1.1's structured fields for marketing and narrative content provide a powerful foundation for LLM integration. By following the guidelines in this document, restaurants can efficiently generate compelling, consistent, and accurate content across multiple channels and languages, enhancing the dining experience while telling authentic stories about their food and values.
