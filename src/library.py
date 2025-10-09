# === SMART NUTRITION APP (Final Robust Version) ===
# USDA + OpenFoodFacts APIs
# Supports: text input, barcode number, image upload
# Converts to imperial units, suggests real alternatives
# Retries input automatically on errors

import requests
from pyzbar.pyzbar import decode
from PIL import Image, ImageEnhance

# for testing
sample_img_path = "src\resources\images\redbull.png"
# --------------------------------------------------
# === UTILITY FUNCTIONS ===
# --------------------------------------------------

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


def display_nutrition_facts(nutrients: dict):
    """Pretty-print nutrition data."""
    if not nutrients:
        print("⚠️ No nutrition data available.")
        return
    print("=" * 50 + f"{nutrients.get('brand_name','')} - {nutrients.get('food_name','Unknown')}" + "=" * 50)
    
    def show(label,key,unit=""):
        v = nutrients.get(key)
        if v is not None:
            print(f"{label:<20}{v:>10} {unit}")
    show("Calories","calories","kcal")
    show("Protein","protein","g")
    show("Total Fat","fat","g")
    show("Carbohydrates","carbohydrates","g")
    show("Sugars","sugars","g")
    show("Dietary Fiber","fiber","g")
    show("Sodium","sodium","mg")
    print(f"Basis: {nutrients.get('unit_basis','per 100 g')}")
    print("=" * 50)


def recommend_healthier_alternative_real(food_name: str, max_results: int = 3):
    """Use OpenFoodFacts to find real healthier alternatives."""
    print(f"\n🔍 Searching OpenFoodFacts for healthier alternatives to: {food_name}")
    print("-" * 60)
    try:
        url = "https://world.openfoodfacts.org/cgi/search.pl"
        params = {"search_terms": food_name, "search_simple": 1,
                  "action": "process", "json": 1, "page_size": 20}
        r = requests.get(url, params=params)
        r.raise_for_status()
        data = r.json()
        products = data.get("products", [])
        if not products:
            print("⚠️ No similar products found.")
            return
        candidates=[]
        for p in products:
            if "nutriments" not in p: continue
            n=p["nutriments"]
            if all(k in n for k in ("energy-kcal_100g","sugars_100g","fat_100g")):
                candidates.append({
                    "name":p.get("product_name","Unknown"),
                    "brand":p.get("brands","Unknown brand"),
                    "url":p.get("url",""),
                    "calories":n["energy-kcal_100g"],
                    "sugars":n["sugars_100g"],
                    "fat":n["fat_100g"]
                })
        if not candidates:
            print("⚠️ No nutrition data found for alternatives.")
            return
        ranked=sorted(candidates,key=lambda x:x["calories"]+2*x["sugars"]+2*x["fat"])
        print(f"✅ Top {max_results} Healthier Alternatives:")
        print("="*60)
        for alt in ranked[:max_results]:
            print(f"🍎 {alt['brand']} – {alt['name']}")
            print(f"   Calories: {alt['calories']} kcal/100 g")
            print(f"   Sugars:   {alt['sugars']} g")
            print(f"   Fat:      {alt['fat']} g")
            if alt['url']:
                print(f"   🔗 {alt['url']}")
            print("-"*60)
    except Exception as e:
        print("⚠️ Error fetching alternatives:",e)


# --------------------------------------------------
# === USDA + OpenFoodFacts DATA FETCHING ===
# --------------------------------------------------

def parse_usda_nutrients(food: dict) -> dict:
    """Extract main nutrients from USDA food entry."""
    nutrients={
        "food_name":food.get("description","Unknown"),
        "brand_name":food.get("brandOwner","Generic/USDA"),
        "calories":None,"protein":None,"fat":None,
        "carbohydrates":None,"sodium":None,"fiber":None,"sugars":None
    }
    for n in food.get("foodNutrients",[]):
        name=n.get("nutrientName","").lower()
        val=n.get("value",0)
        unit=n.get("unitName","").lower()
        if "energy" in name and "kcal" in unit: nutrients["calories"]=val
        elif "protein" in name: nutrients["protein"]=val
        elif "total lipid" in name or "fat" in name: nutrients["fat"]=val
        elif "carbohydrate" in name: nutrients["carbohydrates"]=val
        elif "fiber" in name: nutrients["fiber"]=val
        elif "sugars" in name: nutrients["sugars"]=val
        elif "sodium" in name: nutrients["sodium"]=val
    return nutrients


def get_usda_food(food_name_or_upc: str, api_key: str) -> dict:
    """Try USDA FoodData Central search by name or UPC."""
    url="https://api.nal.usda.gov/fdc/v1/foods/search"
    params={"query":food_name_or_upc,"pageSize":1,"api_key":api_key}
    try:
        r=requests.get(url,params=params)
        r.raise_for_status()
        data=r.json()
        if not data.get("foods"):
            return {}
        return parse_usda_nutrients(data["foods"][0])
    except Exception:
        return {}


def get_openfoodfacts_food(upc: str) -> dict:
    """Fetch nutrient data from OpenFoodFacts by barcode."""
    try:
        r=requests.get(f"https://world.openfoodfacts.org/api/v0/product/{upc}.json")
        r.raise_for_status()
        d=r.json()
        if d.get("status")!=1:
            return {}
        p=d["product"]
        n=p.get("nutriments",{})
        return {
            "food_name":p.get("product_name","Unknown product"),
            "brand_name":p.get("brands","Unknown brand"),
            "calories":n.get("energy-kcal_100g"),
            "protein":n.get("proteins_100g"),
            "fat":n.get("fat_100g"),
            "carbohydrates":n.get("carbohydrates_100g"),
            "fiber":n.get("fiber_100g"),
            "sugars":n.get("sugars_100g"),
            "sodium":n.get("sodium_100g", n.get("salt_100g",0)*400 if "salt_100g" in n else 0)
        }
    except Exception:
        return {}

# --------------------------------------------------
# === BARCODE SCANNING (Colab) ===
# --------------------------------------------------

def decode_barcode_from_image():
    """"""
    img=Image.open(sample_img_path).convert("L")
    img=img.resize((img.width*3,img.height*3))
    img=ImageEnhance.Contrast(img).enhance(2.0)
    codes=decode(img)
    if codes:
        upc=codes[0].data.decode("utf-8")
        print(f"✅ Barcode detected: {upc}")
        return upc
    print("❌ No barcode detected.")
    return None

# --------------------------------------------------
# === MAIN APP LOGIC WITH RETRY ===
# --------------------------------------------------

USDA_API_KEY="DEMO_KEY"  # Get one free at fdc.nal.usda.gov/api-key-signup.html

def run_app():
    print("🥗 Welcome to the Smart Nutrition App!")
    print("1️⃣ Search by food name (e.g., '1 cup rice')")
    print("2️⃣ Search by barcode number (UPC)")
    print("3️⃣ Upload barcode image (Colab)")

    while True:
        choice=input("\nEnter choice (1/2/3): ").strip()

        if choice not in {"1","2","3"}:
            print("❌ Invalid option. Please try again.")
            continue

        try:
            if choice=="1":
                food=input("Enter a food name: ").strip()
                nutrients=get_usda_food(food,USDA_API_KEY) or get_openfoodfacts_food(food)
                if not nutrients:
                    print("⚠️ No data found. Try again.")
                    continue
                nutrients=convert_to_imperial_units(nutrients)
                display_nutrition_facts(nutrients)
                recommend_healthier_alternative_real(food)

            elif choice=="2":
                upc=input("Enter UPC/barcode number: ").strip()
                nutrients=get_usda_food(upc,USDA_API_KEY) or get_openfoodfacts_food(upc)
                if not nutrients:
                    print("⚠️ Invalid barcode or no data found. Try again.")
                    continue
                nutrients=convert_to_imperial_units(nutrients)
                display_nutrition_facts(nutrients)
                recommend_healthier_alternative_real(nutrients.get("food_name",""))

            elif choice=="3":
                upc=decode_barcode_from_image()
                if not upc:
                    print("⚠️ Couldn’t read barcode. Try again.")
                    continue
                nutrients=get_usda_food(upc,USDA_API_KEY) or get_openfoodfacts_food(upc)
                if not nutrients:
                    print("⚠️ No data for this barcode. Try again.")
                    continue
                nutrients=convert_to_imperial_units(nutrients)
                display_nutrition_facts(nutrients)
                recommend_healthier_alternative_real(nutrients.get("food_name",""))

        except Exception as e:
            print("⚠️ An unexpected error occurred:", e)
            print("Let's try that again.")
            continue

        again=input("\nWould you like to search another item? (y/n): ").strip().lower()
        if again!="y":
            print("👋 Goodbye! Stay healthy!")
            break

# Run the app
run_app()

