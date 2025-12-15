class NutritionAnalyzer:
    """
    Analyzes nutritional data for food items and provides formatted output, conversions, comparisons, and health scores.
    """

    def __init__(self):
        # self._nutrients 
        # self._food_name 
        # self._brand_name
        pass


    

    # @property
    # def nutrients(self) -> dict:
    #     return self._nutrients

    # @nutrients.setter
    # def nutrients(self, new_data: dict):
    #     if not isinstance(new_data, dict):
    #         raise ValueError("New nutrient data must be a dictionary.")
    #     self._nutrients = new_data

    # @property
    # def food_name(self) -> str:
    #     return self._food_name

    # @property
    # def brand_name(self) -> str:
    #     return self._brand_name

    # def convert_to_imperial_units(self) -> dict:
    #     """Convert metric nutrient values (per 100 g) into imperial units (per oz)."""
    #     if not nutrients:
    #         return {}
    #     converted = nutrients.copy()
    #     GRAMS_PER_OUNCE = 28.3495
    #     per_oz_factor = GRAMS_PER_OUNCE / 100.0
    #     for key in ["fat", "carbohydrates", "protein", "fiber", "sugars"]:
    #         if key in converted and converted[key] is not None:
    #             converted[key] = round(converted[key] * per_oz_factor, 2)
    #     if "sodium" in converted and converted["sodium"] is not None:
    #         converted["sodium"] = round(converted["sodium"] * per_oz_factor, 1)
    #     if "calories" in converted and converted["calories"] is not None:
    #         converted["calories"] = round(converted["calories"] * per_oz_factor, 1)

    #     converted["unit_basis"] = "per ounce (~28 g)"
        
    #     return converted
    
    def format_nutrition_facts(self, nutrients) -> str:
        
        """Return a formatted string showing nutrition data."""
        
        if not nutrients:
            return "No nutrition data available."
        
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


    # def calculate_nutri_score_letter(self) -> str:
    #     """Calculates Nutri-Score letter grade (A to E) based on nutrient profile."""

    #     try:
    #         sugar = self._nutrients.get('sugars', 0)
    #         sat_fat = self._nutrients.get('saturated_fat', 0)
    #         sodium = self._nutrients.get('sodium', 0)
    #         fiber = self._nutrients.get('fiber', 0)
    #         protein = self._nutrients.get('protein', 0)
    #         fruits_veg = self._nutrients.get('fruits_vegetables', 0)        
    #     except (TypeError, ValueError):
    #         raise ValueError("Invalid nutrient values provided.")

    #     # Negative points
    #     negative = sugar * 2 + sat_fat * 3 + sodium * 1.5

    #     # Positive points
    #     positive = fiber * 2 + protein * 1.5 + fruits_veg * 2

    #     score = round(negative - positive)

    #     # Map score to Nutri-Score letter
    #     if score <= -1:
    #         return 'A'
    #     elif score <= 2:
    #         return 'B'
    #     elif score <= 10:
    #         return 'C'
    #     elif score <= 18:
    #         return 'D'
    #     else:
    #         return 'E'


    def get_healthier_alternatives(self, fooditems: list):
        """
        Args: list of FoodItems

        Returns: Dictionary of 3 alternative FoodItems: highest protein content, lowest calorie, lowest fat content  
        """
        min_calories = -1
        max_protein_per = 0 #per calorie
        min_fat_per = -1 #per calorie

        
        foodRecs ={"protein": None, "fat": None, "calorie": None}
        for val in fooditems:
            pro_per = val.protein/val.calorie
            if  pro_per> max_protein_per:
                foodRecs["protein"] = val
                max_protein_per = pro_per

            if val.calorie < min_calories or min_calories == -1:
                foodRecs["calorie"] = val
                min_calories = val.calorie

            fat_per= val.fat/val.calorie
            if  fat_per < min_fat_per or min_fat_per == -1:
                foodRecs["fat"] = val
                min_fat_per = fat_per 

        return foodRecs
            

    #     try:
    #         url = "https://world.openfoodfacts.org/cgi/search.pl"
    #         params = {
    #             "search_terms": self._food_name,
    #             "search_simple": 1,
    #             "action": "process",
    #             "json": 1,
    #             "page_size": 20
    #             }
            
    #         r = requests.get(url, params=params)
    #         r.raise_for_status()
    #         data = r.json()
    #         products = data.get("products", [])
    #         if not products:
    #             return []
            
    #         candidates = []
    #         for p in products:
    #             if "nutriments" not in p:
    #                 continue
                
    #             n = p["nutriments"]
    #             if all(k in n for k in ("energy-kcal_100g", "sugars_100g", "fat_100g")):
    #                 candidates.append({
    #                     "name": p.get("product_name", "Unknown"),
    #                     "brand": p.get("brands", "Unknown brand"),
    #                     "url": p.get("url", ""),
    #                     "calories": n["energy-kcal_100g"],
    #                     "sugars": n["sugars_100g"],
    #                     "fat": n["fat_100g"]
    #                 })
                
    #         if not candidates:
    #             return []
            
    #         ranked = sorted(candidates, key=lambda x: x["calories"] + 2*x["sugars"] + 2*x["fat"])
    #         return ranked[:max_results]
        
    #     except Exception as e:
    #         print("⚠️ Error fetching alternatives:", e)
    #         return []


    
    # def compare_labels(self, other_nutrients: dict) -> dict:
    #     """
    #     Compare nutrient facts between this food item and another.

    #     Args:
    #         other_nutrients (dict): Nutrient data for the other product.

    #     Returns:
    #         dict: Comparison result for each shared nutrient in the format:
    #               {nutrient: (value_in_self, value_in_other, comparison)}

    #     Raises:
    #         ValueError: If inputs are not valid nutrient dictionaries or contain non-numeric values.
        
    #     Example:
    #         >>> analyzer.compare_labels({'calories': 120, 'protein': 5})
    #         {'calories': (150, 120, 'higher in A'), 'protein': (5, 5, 'equal')}
    #     """
        
    #     if not isinstance(other_nutrients, dict):
    #         raise ValueError("Input must be a dictionary containing nutrient data.")
        
    #     comparison_result = {}
    #     common_nutrients = set(self._nutrients.keys()) & set(other_nutrients.keys())
        
    #     for nutrient in common_nutrients:
    #         a_val = self._nutrients.get(nutrient, 0)
    #         b_val = other_nutrients.get(nutrient, 0)
            
    #         if not isinstance(a_val, (int, float)) or not isinstance(b_val, (int, float)):
    #             raise ValueError(f"Nutrient values must be numeric for '{nutrient}'.")
            
    #         if a_val > b_val:
    #             comparison = "higher in A"
                
    #         elif b_val > a_val:
    #             comparison = "higher in B"
                
    #         else:
    #             comparison = "equal"
                
    #         comparison_result[nutrient] = (a_val, b_val, comparison)
        
    #     return comparison_result

    @staticmethod
    def parse_usda_nutrients(food: dict) -> dict:
        """Extract main nutrients from USDA food entry."""

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


    @staticmethod
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


    def compare_food_macros(item1_name: str, item1_macros: dict, item2_name: str, item2_macros: dict):
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

    def create_macro_breakdown(self) -> dict:
        """
        Calculates macro proportions for graphics’ macro_pie_chart.

        Returns:
            dict: Proportions of protein, fat, and carbohydrates.
        """
        macros = ['protein', 'fat', 'carbohydrates']
        values = [self._nutrients.get(m, 0) for m in macros]
        total = sum(values)
        if total == 0:
            return {m: 0 for m in macros}
        return {m: round(v / total * 100, 2) for m, v in zip(macros, values)}

    # ---------------------------
    # String Representations
    # ---------------------------
    def __str__(self):
        return f"{self._brand_name} - {self._food_name}"

    def __repr__(self):
        return f"NutritionAnalyzer(food_name={self._food_name!r}, brand_name={self._brand_name!r})"
