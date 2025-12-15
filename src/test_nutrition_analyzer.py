import unittest
from unittest.mock import MagicMock

# ---- Imports (adjust module names if your filenames differ) ----
from food_item import (
    NutritionItem,
    FoodItem,
    PackagedFood,
    FoundationFoodItem,
    Recipe,
)

# NutritionAnalyzer import (your file should be nutrition_analyzer.py)
from nutrition_analyzer import NutritionAnalyzer

# Profile import (your file should be profile.py)
from profile import Profile


# ------------------------------------------------------------
# Helpers (so tests work even if Profile uses different names)
# ------------------------------------------------------------
def _get_favorites_container(profile_obj):
    """
    Return the attribute that stores favorites.
    Supports common naming patterns.
    """
    for attr in ("favorites", "favorite_foods", "saved_foods", "_favorites"):
        if hasattr(profile_obj, attr):
            return getattr(profile_obj, attr)
    return None


def _add_favorite(profile_obj, food_obj):
    """
    Try to add a FoodItem to a Profile using common method names.
    If no method exists, fall back to appending to a favorites list if present.
    """
    for method_name in ("add_favorite", "add_to_favorites", "save_favorite", "add_food"):
        if hasattr(profile_obj, method_name) and callable(getattr(profile_obj, method_name)):
            getattr(profile_obj, method_name)(food_obj)
            return

    favs = _get_favorites_container(profile_obj)
    if isinstance(favs, list):
        favs.append(food_obj)
        return

    raise AttributeError(
        "Profile must provide an add method (add_favorite/add_food/etc.) "
        "or expose a list attribute (favorites/favorite_foods/etc.)."
    )


# ============================================================
# 1) FoodItem inheritance + ABC enforcement
# ============================================================
class TestFoodItemInheritance(unittest.TestCase):
    def test_fooditem_is_nutritionitem(self):
        food = FoodItem("Oats", {"fat": 5, "protein": 10, "carbs": 60})
        self.assertIsInstance(food, NutritionItem)

    def test_packagedfood_is_fooditem(self):
        pf = PackagedFood("Protein Shake", {"fat": 2, "protein": 25, "carbs": 5}, servings=2)
        self.assertIsInstance(pf, FoodItem)
        self.assertIsInstance(pf, NutritionItem)

    def test_foundationfooditem_is_fooditem(self):
        ff = FoundationFoodItem(
            name="Banana",
            nutrients={"fat": 0.3, "protein": 1.1, "carbs": 23},
            common_name="Banana",
            scientific_name="Musa",
        )
        self.assertIsInstance(ff, FoodItem)
        self.assertIsInstance(ff, NutritionItem)

    def test_cannot_instantiate_abstract_nutritionitem(self):
        # ABC should not be instantiable
        with self.assertRaises(TypeError):
            NutritionItem("AbstractThing")  # missing abstract methods


# ============================================================
# 2) FoodItem polymorphism (overridden total_calories etc.)
# ============================================================
class TestFoodItemPolymorphism(unittest.TestCase):
    def test_total_calories_polymorphic(self):
        base = FoodItem("Base", {"fat": 1, "protein": 1, "carbs": 1})   # 9 + 4 + 4 = 17
        packaged = PackagedFood("Pack", {"fat": 1, "protein": 1, "carbs": 1}, servings=3)

        self.assertEqual(base.total_calories(), 17)
        self.assertEqual(packaged.total_calories(), 51)  # 17 * 3

    def test_nutrient_summary_overridden(self):
        base = FoodItem("Base", {"fat": 1, "protein": 1, "carbs": 1})
        packaged = PackagedFood("Pack", {"fat": 1, "protein": 1, "carbs": 1}, servings=2)

        self.assertIsInstance(base.nutrient_summary(), str)
        self.assertIsInstance(packaged.nutrient_summary(), str)
        # PackagedFood summary should include serving detail
        self.assertIn("serving", packaged.nutrient_summary().lower())


# ============================================================
# 3) Composition inside food_item.py (Recipe has ingredients)
# ============================================================
class TestRecipeComposition(unittest.TestCase):
    def test_recipe_has_ingredients(self):
        r = Recipe("Trail Mix")
        self.assertIsInstance(r, NutritionItem)

        nuts = FoodItem("Nuts", {"fat": 15, "protein": 6, "carbs": 6})
        fruit = FoodItem("Dried Fruit", {"fat": 0, "protein": 1, "carbs": 25})
        r.add_ingredient(nuts)
        r.add_ingredient(fruit)

        self.assertEqual(len(r.ingredients), 2)
        # total calories should be sum of ingredients (composition)
        self.assertGreater(r.total_calories(), 0)


# ============================================================
# 4) NutritionAnalyzer (Tidjani) — alternatives scoring/sorting
# ============================================================
class TestAnalyzerAlternatives(unittest.TestCase):
    def setUp(self):
        # Your NutritionAnalyzer __init__ requires food_name + brand_name
        self.analyzer = NutritionAnalyzer({"food_name": "Test Food", "brand_name": "Test Brand"})

        self.a = FoodItem("A", {"protein": 10, "fat": 5, "carbs": 20})
        self.b = FoodItem("B", {"protein": 30, "fat": 2, "carbs": 10})
        self.c = FoodItem("C", {"protein": 5,  "fat": 1, "carbs": 30})

    def test_scoring_helpers_exist(self):
        # These methods should exist if you added the Project 4 feature
        self.assertTrue(hasattr(self.analyzer, "protein_per_calorie"))
        self.assertTrue(hasattr(self.analyzer, "fat_per_calorie"))

    def test_sorting_helpers_exist(self):
        self.assertTrue(hasattr(self.analyzer, "sort_high_protein"))
        self.assertTrue(hasattr(self.analyzer, "sort_low_fat"))
        self.assertTrue(hasattr(self.analyzer, "sort_low_calorie"))

    def test_find_alternatives_integration_with_fcmanager_mock(self):
        """
        Integration behavior:
        NutritionAnalyzer uses FCManager.searchDB() to get FoodItems,
        then returns ranked alternatives for 3 criteria.
        """
        # Your analyzer method might be named find_alternatives OR get_healthier_alternatives.
        method = None
        if hasattr(self.analyzer, "find_alternatives"):
            method = self.analyzer.find_alternatives
        elif hasattr(self.analyzer, "get_healthier_alternatives"):
            # only use if your implementation is the FCManager-based one
            method = self.analyzer.get_healthier_alternatives

        self.assertIsNotNone(method, "Missing alternatives method: add find_alternatives(...) to NutritionAnalyzer.")

        mock_fc = MagicMock()
        mock_fc.searchDB.return_value = [self.a, self.b, self.c]

        # For find_alternatives(fc_manager, keyword, limit)
        try:
            result = method(mock_fc, "test", limit=2)
        except TypeError:
            # Some versions may use max_results or different param name
            result = method(mock_fc, "test", 2)

        self.assertIn("highest_protein_per_cal", result)
        self.assertIn("lowest_fat_per_cal", result)
        self.assertIn("lowest_calorie", result)

        # Highest protein-per-cal should be B
        self.assertEqual(result["highest_protein_per_cal"][0].name, "B")
        # Lowest fat-per-cal should be C (fat 1, calories higher but ratio lowest)
        self.assertEqual(result["lowest_fat_per_cal"][0].name, "C")
        # Lowest absolute calories is usually the one with smallest macro total; here B is likely lowest
        # But we’ll compute expected to avoid assumptions:
        lowest = min([self.a, self.b, self.c], key=lambda f: f.total_calories())
        self.assertEqual(result["lowest_calorie"][0].name, lowest.name)


# ============================================================
# 5) Profile ↔ FoodItem composition integration (Tidjani)
# ============================================================
class TestProfileFoodItemComposition(unittest.TestCase):
    def setUp(self):
        # Profile constructor varies across teams; try common patterns
        try:
            self.profile = Profile("tidjani")
        except TypeError:
            # fallback if Profile expects (height, weight) or other values
            self.profile = Profile(0, 0)

        self.food = FoodItem("Greek Yogurt", {"protein": 15, "fat": 2, "carbs": 6})

    def test_profile_is_not_fooditem(self):
        self.assertNotIsInstance(self.profile, FoodItem)
        self.assertNotIsInstance(self.profile, NutritionItem)

    def test_profile_can_store_fooditems(self):
        _add_favorite(self.profile, self.food)
        favs = _get_favorites_container(self.profile)
        self.assertIsNotNone(favs, "Profile does not expose a favorites container attribute.")
        self.assertIn(self.food, favs)

    def test_fooditem_behavior_preserved_when_stored(self):
        _add_favorite(self.profile, self.food)
        favs = _get_favorites_container(self.profile)
        stored = favs[0]
        self.assertEqual(stored.name, "Greek Yogurt")
        self.assertGreater(stored.total_calories(), 0)

    def test_profile_fooditem_to_analyzer_integration(self):
        """
        Integration: Profile stores a FoodItem, then we construct NutritionAnalyzer
        using the FoodItem's values to verify workflow compatibility.
        """
        _add_favorite(self.profile, self.food)
        favs = _get_favorites_container(self.profile)
        stored = favs[0]

        analyzer = NutritionAnalyzer({
            "food_name": stored.name,
            "brand_name": "ProfileSaved",
            "protein": stored.nutrients.get("protein", 0),
            "fat": stored.nutrients.get("fat", 0),
            "carbohydrates": stored.nutrients.get("carbs", 0),  # FoodItem uses "carbs"
        })

        # Just verify it doesn't crash and returns a valid grade
        grade = analyzer.calculate_nutri_score_letter()
        self.assertIn(grade, ["A", "B", "C", "D", "E"])


if __name__ == "__main__":
    unittest.main()
