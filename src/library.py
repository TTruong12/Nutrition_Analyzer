# Function Library

# --------------------------------------------------
# Install dependencies (only needed once per Colab session)
# --------------------------------------------------
#!apt-get install -y libzbar0 > /dev/null
#!pip install -q pyzbar pillow requests
#from google.colab import files

import json
import csv
import requests
from pyzbar.pyzbar import decode
from PIL import Image, ImageEnhance
from typing import List, Dict
from html.parser import HTMLParser
import os
import matplotlib.pyplot as plt
import numpy as np

# --------------------------------------------------
# === UTILITY FUNCTIONS ===
# --------------------------------------------------
# Aneesh Parkhie comment on code below: Consider logging or warning if a nutrient key is missing (for debugging)
def convert_to_imperial_units(nutrients: dict) -> dict:
    """Convert metric nutrient values (per 100 g) into imperial units (per oz)."""
    if not nutrients:
        return {}
    converted = nutrients.copy()
    GRAMS_PER_OUNCE = 28.3495
    per_oz_factor = GRAMS_PER_OUNCE / 100.0
    for key in ["fat", "carbohydrates", "protein", "fiber", "sugars"]:
        if key in converted and converted[key] is not None:
            converted[key] = round(converted[key] * per_oz_factor, 2)
    if "sodium" in converted and converted["sodium"] is not None:
        converted["sodium"] = round(converted["sodium"] * per_oz_factor, 1)
    if "calories" in converted and converted["calories"] is not None:
        converted["calories"] = round(converted["calories"] * per_oz_factor, 1)
    converted["unit_basis"] = "per ounce (~28 g)"
    return converted


def format_nutrition_facts(nutrients: dict) -> str:
    """Return a formatted string showing nutrition data."""
    if not nutrients:
        return "⚠️ No nutrition data available."

    lines = []
    lines.append("=" * 50)
    lines.append(f"{nutrients.get('brand_name', '')} - {nutrients.get('food_name', 'Unknown')}")
    lines.append("=" * 50)

    def show(label, key, unit=""):
        v = nutrients.get(key)
        if v is not None:
            lines.append(f"{label:<20}{v:>10} {unit}")

    show("Calories", "calories", "kcal")
    show("Protein", "protein", "g")
    show("Total Fat", "fat", "g")
    show("Carbohydrates", "carbohydrates", "g")
    show("Sugars", "sugars", "g")
    show("Dietary Fiber", "fiber", "g")
    show("Sodium", "sodium", "mg")

    lines.append(f"Basis: {nutrients.get('unit_basis', 'per 100 g')}")
    lines.append("=" * 50)

    return "\n".join(lines)


def display_nutrition_facts(nutrients: dict):
    """Display nutrition facts using the formatted output."""
    formatted = format_nutrition_facts(nutrients)
    print(formatted)

def calculate_nutri_score_letter(nutrients: dict) -> str:
    """
    Calculates Nutri-Score letter grade (A to E) based on nutrient profile.
 
    """
    try:
        sugar = float(nutrients.get('sugar', 0))
        sat_fat = float(nutrients.get('saturated_fat', 0))
        sodium = float(nutrients.get('sodium', 0))
        fiber = float(nutrients.get('fiber', 0))
        protein = float(nutrients.get('protein', 0))
        fruits_veg = float(nutrients.get('fruits_veg_percent', 0))
    except (TypeError, ValueError):
        raise ValueError("Invalid nutrient values provided.")

    # Negative points
    negative = sugar * 2 + sat_fat * 3 + sodium * 1.5

    # Positive points
    positive = fiber * 2 + protein * 1.5 + fruits_veg * 2

    score = round(negative - positive)

    # Map score to Nutri-Score letter
    if score <= -1:
        return 'A'
    elif score <= 2:
        return 'B'
    elif score <= 10:
        return 'C'
    elif score <= 18:
        return 'D'
    else:
        return 'E'

# --------------------------------------------------
# === HEALTHIER ALTERNATIVES (NEW MODULAR VERSION) ===
# --------------------------------------------------

def get_healthier_alternatives(food_name: str, max_results: int = 3) -> list:
    """Fetch and rank healthier alternatives from OpenFoodFacts for a given food."""
    print(f"\n🔍 Searching OpenFoodFacts for healthier alternatives to: {food_name}")
    print("-" * 60)
    try:
        url = "https://world.openfoodfacts.org/cgi/search.pl"
        params = {
            "search_terms": food_name,
            "search_simple": 1,
            "action": "process",
            "json": 1,
            "page_size": 20
        }
        r = requests.get(url, params=params)
        r.raise_for_status()
        data = r.json()
        products = data.get("products", [])
        if not products:
            print("⚠️ No similar products found.")
            return []

        candidates = []
        for p in products:
            if "nutriments" not in p:
                continue
            n = p["nutriments"]
            if all(k in n for k in ("energy-kcal_100g", "sugars_100g", "fat_100g")):
                candidates.append({
                    "name": p.get("product_name", "Unknown"),
                    "brand": p.get("brands", "Unknown brand"),
                    "url": p.get("url", ""),
                    "calories": n["energy-kcal_100g"],
                    "sugars": n["sugars_100g"],
                    "fat": n["fat_100g"]
                })

        if not candidates:
            print("⚠️ No nutrition data found for alternatives.")
            return []

        ranked = sorted(candidates, key=lambda x: x["calories"] + 2*x["sugars"] + 2*x["fat"])
        return ranked[:max_results]

    except Exception as e:
        print("⚠️ Error fetching alternatives:", e)
        return []


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

def compare_labels(product_a: dict, product_b: dict) -> dict:
    """
    Compare nutrient facts between two food products.
    
    """
    if not isinstance(product_a, dict) or not isinstance(product_b, dict):
        raise ValueError("Both inputs must be dictionaries containing nutrient data.")

    comparison_result = {}
    common_nutrients = set(product_a.keys()) & set(product_b.keys())

    for nutrient in common_nutrients:
        a_val = product_a.get(nutrient, 0)
        b_val = product_b.get(nutrient, 0)

        if not isinstance(a_val, (int, float)) or not isinstance(b_val, (int, float)):
            raise ValueError(f"Nutrient values must be numeric for '{nutrient}'.")

        if a_val > b_val:
            comparison = "higher in A"
        elif b_val > a_val:
            comparison = "higher in B"
        else:
            comparison = "equal"

        comparison_result[nutrient] = (a_val, b_val, comparison)

    return comparison_result

# --------------------------------------------------
# === USDA + OpenFoodFacts DATA FETCHING ===
# --------------------------------------------------

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


def get_usda_food(food_name_or_upc: str, api_key: str) -> dict:
    """Try USDA FoodData Central search by name or UPC."""
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {"query": food_name_or_upc, "pageSize": 1, "api_key": api_key}
    try:
        r = requests.get(url, params=params)
        r.raise_for_status()
        data = r.json()
        if not data.get("foods"):
            return {}
        return parse_usda_nutrients(data["foods"][0])
    except Exception:
        return {}



def get_openfoodfacts_food(upc: str) -> dict:
    """Fetch nutrient data from OpenFoodFacts by barcode."""
    try:
        r = requests.get(f"https://world.openfoodfacts.org/api/v0/product/{upc}.json")
        r.raise_for_status()
        d = r.json()
        if d.get("status") != 1:
            return {}
        p = d["product"]
        n = p.get("nutriments", {})
        return {
            "food_name": p.get("product_name", "Unknown product"),
            "brand_name": p.get("brands", "Unknown brand"),
            "calories": n.get("energy-kcal_100g"),
            "protein": n.get("proteins_100g"),
            "fat": n.get("fat_100g"),
            "carbohydrates": n.get("carbohydrates_100g"),
            "fiber": n.get("fiber_100g"),
            "sugars": n.get("sugars_100g"),
            "sodium": n.get("sodium_100g", n.get("salt_100g", 0) * 400 if "salt_100g" in n else 0)
        }
    except Exception:
        return {}
        
def search_keyword(text: str, keyword: str) -> bool:
    """
    Search for a keyword in a block of text.
    """
    if not isinstance(text, str) or not isinstance(keyword, str):
        raise ValueError("Both text and keyword must be strings.")

    return keyword.lower() in text.lower()

def format_search_results(results: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Clean and format a list of search result entries containing brand and product names.
    """

    class HTMLCleaner(HTMLParser):
        def __init__(self):
            super().__init__()
            self.text_parts = []

        def handle_data(self, data):
            self.text_parts.append(data)

        def get_clean_text(self):
            return ''.join(self.text_parts).strip()

    def clean_text(text: str) -> str:
        if not isinstance(text, str):
            raise ValueError("Text must be a string.")
        parser = HTMLCleaner()
        parser.feed(text)
        raw = parser.get_clean_text()
        allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!? -"
        return ''.join(c for c in raw if c in allowed).strip()

    if not isinstance(results, list):
        raise ValueError("Input must be a list of dictionaries.")

    formatted = []
    for entry in results:
        if not all(k in entry for k in ('brand', 'product')):
            continue

        brand = clean_text(entry['brand'])
        product = clean_text(entry['product'])

        if brand and product:
            formatted.append({'brand': brand, 'product': product})

    return formatted


food_url = "https://api.nal.usda.gov/fdc/v1"
USDA_API_KEY = "DEMO_KEY"  # Replace with your USDA key


def get_food_item(upc): #Theo
    """Given the universal product code, returns json of details of that item"""
    url = f"{food_url}/foods/search?api_key={USDA_API_KEY}&query={upc}"
    response = requests.get(url)
    if response.status_code == 200:
        food_data = response.json()
        return food_data
    else:
        print(f"Failed to retrieve data {response.status_code}")



def generate_alt(upc, nutrient, comparison, ref, filters=None): #Theo
    """
    Nutrient = nutrient compared
    comparison 0=more, 1=less
    ref: nutrient per ref
    filters: will implement later

    Example:
    generate_alt(0000901626026, sugar, 1, serving)
    Returns food items with less sugar per serving compared to Redbull
    """
    init_food = get_food_item(upc)[0]
    init_nutrient_val = init_food[nutrient]

    url = f"{food_url}/foods/search?api_key={USDA_API_KEY}"

    if comparison == 0:
        response = requests.get(url+f"&{nutrient}>{init_nutrient_val}&sortBy={nutrient}&sortOrder=desc")
        return response.json()
    if comparison == 1:
        pass

    pass


# ----- generate_alt() test ------
# print(get_food_item(850126007120))
test_food = get_food_item(850126007120)
#for key in test_food["foods"][0]["foodNutrients"]:
#    print(key, ":", test_food["foods"][0]["foodNutrients"])
print(test_food["foods"][0]["foodNutrients"][1])


# print(generate_alt(850126007120, "sugar", 0, "serving"))
# --------------------------------


# --------------------------------------------------
# === BARCODE SCANNING (Colab) ===
# --------------------------------------------------

def decode_barcode_from_image():
    """Upload and decode a barcode image."""
    print("📸 Upload an image with a visible barcode …")
    uploaded = files.upload()
    image_path = list(uploaded.keys())[0]
    img = Image.open(image_path).convert("L")
    img = img.resize((img.width * 3, img.height * 3))
    img = ImageEnhance.Contrast(img).enhance(2.0)
    codes = decode(img)
    if codes:
        upc = codes[0].data.decode("utf-8")
        print(f"✅ Barcode detected: {upc}")
        return upc
    print("❌ No barcode detected.")
    return None

# --------------------------------------------------
# === MAIN APP LOGIC WITH RETRY (Updated) ===
# --------------------------------------------------

USDA_API_KEY = "DEMO_KEY"  # Replace with your USDA key
USDA_URL = "https://api.nal.usda.gov/fdc/v1" #URL for the food central database
csv_export = "../resources/export.csv" #holds export dat in csv form 

def get_food_item(upc):
    """Given the universal product code, returns json of details of that item"""
    url = f"{USDA_URL}/food/search?api_key={USDA_API_KEY}&query={upc}"
    response = requests.get(url)
    if response.status_code == 200:
        food_data = response.json()
        return food_data
    else:
        print(f"Failed to retrieve data {response.status_code}")


def prompt_key() -> str:
    """Prompts user for api key"""
    test_key = input("Enter USDA Food Central API key: ")
    return test_key


def set_key(key = "DEMO_KEY"):
    """Sets api key to key parameter if valid key"""
    url = f"{USDA_URL}/food/0000000?api_key={key}"
    response = requests.get(test_url)
    if (response.status_code == 200):
        USDA_API_KEY = test_key
    else:
        pass

def export_to_csv(food_details):
   """Exports selected food's nutritional facts to export.csv"""
    fieldnames = set()
    for entry in food_details:
        fieldnames.update(entry.keys())
    fieldnames = list(fieldnames)

    with open(csv_export, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  # Write headers
        writer.writerows(food_details)  

 
def run_app():
    print("🥗 Welcome to the Smart Nutrition App!")
    print("1️⃣ Search by food name (e.g., '1 cup rice')")
    print("2️⃣ Search by barcode number (UPC)")
    print("3️⃣ Upload barcode image (Colab)")

    while True:
        choice = input("\nEnter choice (1/2/3): ").strip()

        if choice not in {"1", "2", "3"}:
            print("❌ Invalid option. Please try again.")
            continue

        try:
            if choice == "1":
                food = input("Enter a food name: ").strip()
                nutrients = get_usda_food(food, USDA_API_KEY) or get_openfoodfacts_food(food)
                if not nutrients:
                    print("⚠️ No data found. Try again.")
                    continue
                nutrients = convert_to_imperial_units(nutrients)
                display_nutrition_facts(nutrients)
                alternatives = get_healthier_alternatives(food)
                display_healthier_alternatives(alternatives)

            elif choice == "2":
                upc = input("Enter UPC/barcode number: ").strip()
                nutrients = get_usda_food(upc, USDA_API_KEY) or get_openfoodfacts_food(upc)
                if not nutrients:
                    print("⚠️ Invalid barcode or no data found. Try again.")
                    continue
                nutrients = convert_to_imperial_units(nutrients)
                display_nutrition_facts(nutrients)
                alternatives = get_healthier_alternatives(nutrients.get("food_name", ""))
                display_healthier_alternatives(alternatives)

            elif choice == "3":
                upc = decode_barcode_from_image()
                if not upc:
                    print("⚠️ Couldn’t read barcode. Try again.")
                    continue
                nutrients = get_usda_food(upc, USDA_API_KEY) or get_openfoodfacts_food(upc)
                if not nutrients:
                    print("⚠️ No data for this barcode. Try again.")
                    continue
                nutrients = convert_to_imperial_units(nutrients)
                display_nutrition_facts(nutrients)
                alternatives = get_healthier_alternatives(nutrients.get("food_name", ""))
                display_healthier_alternatives(alternatives)

        except Exception as e:
            print("⚠️ An unexpected error occurred:", e)
            print("Let's try that again.")
            continue

        again = input("\nWould you like to search another item? (y/n): ").strip().lower()
        if again != "y":
            print("👋 Goodbye! Stay healthy!")
            break
def parse_search_query(query: str) -> dict:
    query = query.strip().lower()
    filters = []
    possible_filters = ["low sugar", "low fat", "high protein", "high fiber", "gluten free", "vegan"]

    for f in possible_filters:
        if f in query:
            filters.append(f)
            query = query.replace(f, "").strip()

    return {"food": query, "filters": filters}

def show_macro_pie_chart(food_name: str, macros: dict):
    if not all(k in macros for k in ("protein", "carbs", "fat")):
        raise ValueError("macros must contain 'protein', 'carbs', and 'fat' keys.")
    labels = ["Protein", "Carbs", "Fat"]
    values = [macros["protein"], macros["carbs"], macros["fat"]]
    colors = ["#36A2EB", "#FFCE56", "#FF6384"]
    total = sum(values)
    if total == 0:
        raise ValueError("Total macronutrients cannot be zero.")
    percentages = [v / total * 100 for v in values]
    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=[f"{l} ({p:.1f}%)" for l, p in zip(labels, percentages)],
            colors=colors, autopct="%.1f%%", startangle=140)
    plt.title(f"Macronutrient Breakdown: {food_name}", fontsize=14)
    plt.show()

def compare_food_macros(item1_name: str, item1_macros: dict,
                        item2_name: str, item2_macros: dict):
    macros = ["protein", "carbs", "fat"]
    for m in macros:
        if m not in item1_macros or m not in item2_macros:
            raise ValueError("Both macro dicts must contain 'protein', 'carbs', and 'fat'.")
    item1_values = [item1_macros[m] for m in macros]
    item2_values = [item2_macros[m] for m in macros]
    total1, total2 = sum(item1_values), sum(item2_values)
    item1_perc = [v / total1 * 100 for v in item1_values]
    item2_perc = [v / total2 * 100 for v in item2_values]
    x = np.arange(len(macros))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 6))
    bars1 = ax.bar(x - width/2, item1_values, width, label=f"{item1_name} ({int(total1)}g total)")
    bars2 = ax.bar(x + width/2, item2_values, width, label=f"{item2_name} ({int(total2)}g total)")
    for bars, percents in [(bars1, item1_perc), (bars2, item2_perc)]:
        for bar, p in zip(bars, percents):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f"{p:.1f}%",
                    ha='center', va='bottom', fontsize=9)
    ax.set_ylabel("Grams")
    ax.set_title("Macronutrient Comparison")
    ax.set_xticks(x)
    ax.set_xticklabels([m.capitalize() for m in macros])
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show() 

def create_user_profile():
    print("Welcome to NutriTrack Setup!")
    name = input("Enter your name: ").strip().title()
    age = int(input("Enter your age: "))
    gender = input("Enter your gender (M/F): ").strip().upper()
    activity = input("Activity level (low/medium/high): ").strip().lower()
    goal = input("Goal (lose/maintain/gain): ").strip().lower()

    base = 2000 if gender == "M" else 1800
    activity_factor = {"low": 1.2, "medium": 1.5, "high": 1.8}.get(activity, 1.3)
    calories = base * activity_factor

    if goal == "lose":
        calories -= 300
    elif goal == "gain":
        calories += 300

    profile = {"name": name, "age": age, "gender": gender,
               "activity": activity, "goal": goal,
               "daily_calories": round(calories)}
    
    print(f"\nProfile created for {name}! Estimated calories/day: {profile['daily_calories']}")
    return profile

def manage_favorites(food_item: str, filename="favorites.json"):
    food_item = food_item.strip().title()
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                favorites = json.load(f)
            except json.JSONDecodeError:
                favorites = []
    else:
        favorites = []
    if food_item not in favorites:
        favorites.append(food_item)
        with open(filename, "w") as f:
            json.dump(favorites, f, indent=2)
        print(f"✅ '{food_item}' added to your favorites list!")
    else:
        print(f"ℹ️ '{food_item}' is already in your favorites.")
        print("\nYour Favorite Foods:")
    for i, item in enumerate(favorites, 1):
        print(f"{i}. {item}")

    return favorites

def create_and_manage_favorites(list_name: str, new_items: list[str] = None, filename="favorites_db.json"):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = {}
    else:
        data = {}
    
    if list_name not in data:
        data[list_name] = []
        print(f"🆕 Created new favorites list: '{list_name}'")

    if new_items:
        added = 0
        for item in new_items:
            food = item.strip().title()
            if food not in data[list_name]:
                data[list_name].append(food)
                added += 1
        if added:
            print(f"✅ Added {added} new item(s) to '{list_name}'!")
        else:
            print(f"ℹ️ No new items added — all already in '{list_name}'.")

    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

    print(f"\n📋 Favorites in '{list_name}':")
    for i, food in enumerate(data[list_name], 1):
        print(f"{i}. {food}")

    return data[list_name]

# --------------------------------------------------
# Run the app
# --------------------------------------------------

#run_app()
