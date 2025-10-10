Display Nutrition facts: Displays Nutrition Facts
def display_nutrition_facts(nutrients: dict):
    """Display nutrition facts using the formatted output."""
    formatted = format_nutrition_facts(nutrients)
    print(formatted)


    

Outputs healthier foods 
display_healthier_alternatives 
def display_healthier_alternatives(alternatives: list):
    """Display a formatted list of healthier alternatives."""
    if not alternatives:
        print("⚠️ No alternatives available to display.")
        return

    print(f"✅ Top {len(alternatives)} Healthier Alternatives:")
    print("=" * 60)
    for alt in alternatives:
        print(f"🍎 {alt['brand']} – {alt['name']}")
        print(f"   Calories: {alt['calories']} kcal/100 g")
        print(f"   Sugars:   {alt['sugars']} g")
        print(f"   Fat:      {alt['fat']} g")
        if alt['url']:
            print(f"   🔗 {alt['url']}")
        print("-" * 60)


    

