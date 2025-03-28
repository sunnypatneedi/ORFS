# ORFS v1.1 Marketing Guide for Restaurants

## Introduction

This guide is designed to help restaurant marketing teams effectively utilize the enhanced marketing capabilities in ORFS v1.1. The new specification enables you to share rich narratives, local sourcing information, promotional details, and other marketing content through standardized data feeds. By properly implementing these features, you can enhance your digital presence, connect with customers through authentic storytelling, and facilitate seamless integration with reservation platforms, delivery apps, review sites, and other digital services.

## Getting Started with Marketing Extensions

### Core Marketing Fields

ORFS v1.1 introduces a comprehensive `MarketingExtension` that includes:

1. **Loyalty Program Details**
   - Program name and tiers
   - Benefits for each tier
   - Promotional messaging

2. **Promotional Offers**
   - Limited-time specials and discounts
   - Start and end times
   - Marketing copy for each promotion

3. **Social Media Strategy**
   - Platform information
   - Recommended hashtags
   - Posting schedules
   - Pre-written content snippets

4. **Events**
   - Upcoming special events
   - Chef demonstrations
   - Wine tastings or special menus
   - Location and timing details

5. **Website CTAs**
   - Call-to-action button text
   - Target URLs
   - Style guidelines

### Best Practices for Marketing Extensions

- **Keep it current**: Update promotional information regularly as offers change
- **Be specific**: Include precise details about timing, benefits, and exclusions
- **Maintain consistency**: Ensure your marketing copy aligns with your brand voice
- **Track performance**: Use unique URLs and codes to measure the effectiveness of promotions shared through ORFS feeds

## Crafting Compelling Narrative Content

### Available Narrative Fields

ORFS v1.1 includes several narrative fields at the dish and ingredient level:

1. **Chef Content**
   - `chef_highlight`: Short attention-grabbing taglines
   - `chef_story`: Detailed narrative about inspiration or creation
   - `chef_anecdote`: Personal stories or memories related to the dish

2. **Cultural and Seasonal Context**
   - `culinary_philosophy`: Overall approach to food and cooking
   - `seasonal_story`: Why a dish is relevant to the current season
   - `cultural_context`: Historical or cultural background

3. **Ingredient Narratives**
   - `ingredient_story`: Details about special ingredients
   - `supplier_location`: Information about farms and producers
   - `sustainability_impact`: Environmental benefits and practices

### Tips for Effective Storytelling

1. **Be authentic**: Share real stories, not marketing fluff
2. **Keep it concise**: Even detailed narratives should be digestible
3. **Focus on sensory details**: Describe flavors, aromas, and textures
4. **Highlight unique elements**: What makes your dish or ingredients special?
5. **Connect emotionally**: Share the human elements behind your food
6. **Update seasonally**: Refresh content to reflect current offerings

### Example: Creating a Complete Dish Narrative

Below is an example of how different narrative fields work together to tell a compelling story:

```json
{
  "name": "Heirloom Tomato Pizza",
  "chef_highlight": "Chef Maria's tribute to her Italian grandmother",
  "chef_story": "During summers in Naples, I watched my grandmother transform sun-ripened tomatoes into magic on flatbread. This pizza honors her legacy with our modern twist.",
  "ingredient_story": "Our heirloom tomatoes come from Green Valley Farm, where the volcanic soil creates uniquely sweet fruit with complex acidity—perfect for our signature sauce.",
  "seasonal_story": "Late summer brings the peak of tomato season, when these heirlooms develop their most intense flavor. We wait all year for this perfect moment.",
  "sustainability_impact": "By partnering directly with local farmers, we reduce food miles by 75% compared to conventional sourcing, resulting in fresher ingredients and a smaller carbon footprint."
}
```

## Showcasing Local Sourcing

### Supplier Location Data Structure

ORFS v1.1 provides dedicated fields for detailed supplier information:

```json
"supplier_location": {
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
```

### Recommendations for Local Sourcing Data

1. **Get permission**: Always obtain explicit permission from suppliers before sharing their details
2. **Provide options**: Offer both detailed and compact representation options
3. **Update regularly**: Ensure farm information reflects seasonal changes in sourcing
4. **Add certification details**: Include organic, sustainable, or other relevant certifications
5. **Calculate food miles**: Provide accurate distance information when possible
6. **Tell the human story**: Connect the producer to the product with authentic narratives

## Multi-Language Support

### Using TranslatedString

ORFS v1.1 introduces a `TranslatedString` type that allows you to provide content in multiple languages:

```json
"chef_story": {
  "translations": {
    "en": "During summers in Naples, I watched my grandmother transform sun-ripened tomatoes into magic on flatbread. This pizza honors her legacy with our modern twist.",
    "es": "Durante los veranos en Nápoles, vi a mi abuela transformar tomates madurados al sol en magia sobre pan plano. Esta pizza honra su legado con nuestro toque moderno.",
    "it": "Durante le estati a Napoli, guardavo mia nonna trasformare pomodori maturati al sole in magia sulla focaccia. Questa pizza onora il suo patrimonio con il nostro tocco moderno."
  }
}
```

### Translation Strategy

1. **Prioritize key languages**: Focus on the languages most relevant to your customer base
2. **Maintain cultural context**: Adapt cultural references appropriately for each language
3. **Use professional translation**: Invest in quality translations for customer-facing content
4. **Start small**: Begin with your most popular dishes and expand over time
5. **Consider regional dialects**: Adjust translations for specific regional target markets

## Leveraging Bundle Offerings

The new `Bundle` message type allows you to define and promote groups of items sold together:

```json
{
  "id": "date_night_special",
  "bundle_name": "Date Night Special",
  "included_items": ["pizza_margherita", "tiramisu", "wine_chianti"],
  "price": 4500,
  "currency": "USD",
  "bundle_marketing_copy": "Experience an authentic Italian evening with our signature Margherita pizza, homemade tiramisu, and a glass of Chianti—perfect for sharing!"
}
```

### Marketing Bundle Effectively

1. **Create strategic groupings**: Design bundles that make sense culinary and increase average order value
2. **Highlight the value**: Emphasize savings or exclusive items in your bundle marketing copy
3. **Target specific occasions**: Create bundles for date nights, family dinners, or business lunches
4. **Rotate offerings**: Regularly update bundles to maintain interest and reflect seasonal changes
5. **Track performance**: Monitor which bundles sell best and iterate accordingly

## Integration with Digital Platforms

### Working with Delivery Apps

1. **Harmonize descriptions**: Ensure your ORFS narrative content is reflected in delivery app listings
2. **Coordinate promotions**: Sync your ORFS promotional offers with delivery platform specials
3. **Update photography**: Maintain consistency between your ORFS feed and delivery platform imagery

### Reservation System Integration

1. **Promote special events**: Use the events section to highlight experiences that require reservations
2. **Highlight special tables**: Identify prime seating or chef's table experiences
3. **Bundle reservations with experiences**: Create special dining packages

### Website and Social Media Alignment

1. **Maintain voice consistency**: Ensure your ORFS narrative matches your website and social content
2. **Reuse content strategically**: Leverage your ORFS narratives as building blocks for expanded content
3. **Drive traffic with CTAs**: Use the CTA fields to create consistent calls-to-action across platforms

## Measuring Impact

### Key Metrics to Track

1. **Content adoption rate**: Which platforms are using your enhanced ORFS content?
2. **Promotion effectiveness**: Are ORFS-distributed promotions being redeemed?
3. **Menu item performance**: Do items with rich narrative content sell better?
4. **Bundle conversion**: How often are bundles purchased compared to individual items?
5. **Customer engagement**: Is there increased interaction with items featuring local sourcing information?

### Continuous Improvement Process

1. **Review quarterly**: Assess which content types are performing best
2. **Refresh seasonal content**: Update narratives to reflect current offerings
3. **A/B test narratives**: Try different storytelling approaches and measure results
4. **Gather feedback**: Ask customers which stories resonated with them
5. **Train staff**: Ensure in-person storytelling matches your digital narratives

## Conclusion

The marketing extensions in ORFS v1.1 provide a powerful platform for sharing your restaurant's unique story and promotional content with the digital ecosystem. By thoughtfully implementing these capabilities, you can ensure consistent, compelling storytelling across all customer touchpoints while streamlining your marketing operations.

Remember that authentic, well-crafted narratives not only help differentiate your restaurant in a crowded marketplace but also create emotional connections with customers that lead to lasting loyalty.
