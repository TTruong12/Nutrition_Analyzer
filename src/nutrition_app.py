class NutritionApp:
    """
    Main application controller for nutrition analysis and user interaction.
    Coordinates database access, nutrition analysis, and visual display.
    """

    def __init__(self):
        self._db = db_manager.foodcentral()
        self._graphics = Graphics()
        self._profile: Optional[Profile] = None
        self._analyzer = NutritionAnalyzer(self._db)

    def create_user_profile(self):
        w = float(input("Enter your weight (kg): ").strip())
        h = float(input("Enter your height (cm): ").strip())
        self._profile = Profile(w, h)
        print(f"Profile created. BMI: {self._profile.calculate_bmi()}")

    def run(self):
        print("Welcome to the Nutrition App")
        while True:
            choice = input("1) Search food  2) Create profile  3) Quit: ").strip()
            if choice == "1":
                query = input("Enter food name or UPC: ").strip()
                result = self._analyzer.lookup(query)
                if not result:
                    print("No nutrition data found.")
                    continue
                food = FoodItem(result["food_name"], result["nutrients"])
                self._graphics.display_nutrition_facts({
                    "food_name": food.name,
                    "protein": food.nutrients.get("protein"),
                    "fat": food.nutrients.get("fat"),
                    "carbohydrates": food.nutrients.get("carbs"),
                    "unit_basis": "per 100 g"
                })
                self._graphics.show_macro_pie_chart(food.name, food.nutrients)
            elif choice == "2":
                self.create_user_profile()
            elif choice == "3":
                print("Goodbye.")
                break
            else:
                print("Invalid option.")

    def __str__(self):
        return f"NutritionApp(Profile={self._profile})"

    def __repr__(self):
        return f"NutritionApp(db={self._db!r}, profile={self._profile!r})"





