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


convert_to_imperial: This makes all the units imperial system


def convert_to_imperial_units(nutrients: dict) -> dict:
    """Convert nutrient values from per 100 g to per ounce (~28 g)."""
    if not nutrients: return {}
    converted = nutrients.copy()
    f = 28.3495 / 100
    for k in ["fat", "carbohydrates", "protein", "fiber", "sugars", "sodium", "calories"]:
        if k in converted and converted[k] is not None:
            converted[k] = round(converted[k] * f, 2 if k not in {"sodium", "calories"} else 1)
    converted["unit_basis"] = "per ounce (~28 g)"
    return converted


parse_usda_nutrients: sorts nutrients from USDA API

def parse_usda_nutrients(food: dict) -> dict:
    """Extract main nutrients from USDA food entry."""
    nutrients = {
        "food_name": food.get("description", "Unknown"),
        "brand_name": food.get("brandOwner", "Generic/USDA"),
        "calories": None, "protein": None, "fat": None,
        "carbohydrates": None, "sodium": None, "fiber": None, "sugars": None
    }
    for n in food.get("foodNutrients", []):
        name = n.get("nutrientName", "").lower()
        val = n.get("value", 0)
        unit = n.get("unitName", "").lower()
        if "energy" in name and "kcal" in unit:
            nutrients["calories"] = val
        elif "protein" in name:
            nutrients["protein"] = val
        elif "total lipid" in name or "fat" in name:
            nutrients["fat"] = val
        elif "carbohydrate" in name:
            nutrients["carbohydrates"] = val
        elif "fiber" in name:
            nutrients["fiber"] = val
        elif "sugars" in name:
            nutrients["sugars"] = val
        elif "sodium" in name:
            nutrients["sodium"] = val
    return nutrients





    

    

