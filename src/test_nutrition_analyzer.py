import unittest
from unittest.mock import MagicMock

from food_item import FoodItem, BrandedFoodItem
from nutrition_analyzer import NutritionAnalyzer
from profile import Profile


# ============================================================
# 1) FoodItem Base Behavior + Inheritance (Tidjani)
# ============================================================
class TestFoodItemInheritance(unittest.TestCase):

    def test_fooditem_creation(self):
        food = FoodItem("Oats", {"protein": 10, "fat": 5, "carbs": 60})
        self.assertEqual(food.name, "Oats")
        self.assertIsInstance(food, FoodItem)

    def test_brandedfooditem_is_fooditem(self):
        branded = BrandedFoodItem(
            name="Protein Bar",
            nutrients={"protein": 20, "fat": 8, "carbs": 22},
            brand_name="TestBrand"
        )
        self.assertIsInstance(branded, FoodItem)
        self.assertEqual(branded.brand_name, "TestBrand")

    def test_total_calories_polymorphic(self):
        base = FoodItem("Base", {"protein": 1, "fat": 1, "carbs": 1})
        branded = BrandedFoodItem(
            name="Branded",
            nutrients={"protein": 1, "fat": 1, "carbs": 1},
            brand_name="BrandX"
        )
        self.assertEqual(base.total_calories(), 17)
        self.assertEqual(branded.total_calories(), 17)


# ============================================================
# 2) NutritionAnalyzer Core Functionality (Tidjani)
# ============================================================
class TestNutritionAnalyzer(unittest.TestCase):

    def setUp(self):
        self.food = FoodItem("Greek Yogurt", {"protein": 15, "fat": 2, "carbs": 6})

        self.analyzer = NutritionAnalyzer({
            "food_name": self.food.name,
            "brand_name": "Generic",
            "protein": 15,
            "fat": 2,
            "carbohydrates": 6
        })

    def test_nutri_score_returns_valid_letter(self):
        grade = self.analyzer.calculate_nutri_score_letter()
        self.assertIn(grade, ["A", "B", "C", "D", "E"])

    def test_macro_breakdown_sums_to_100(self):
        breakdown = self.analyzer.create_macro_breakdown()
        self.assertAlmostEqual(sum(breakdown.values()), 100, delta=0.1)


# ============================================================
# 3) Integration: NutritionAnalyzer + FCManager (Mocked)
# ============================================================
class TestAnalyzerAlternativesIntegration(unittest.TestCase):

    def setUp(self):
        self.analyzer = NutritionAnalyzer({
            "food_name": "Test Food",
            "brand_name": "Test Brand"
        })

        self.a = FoodItem("A", {"protein": 10, "fat": 5, "carbs": 20})
        self.b = FoodItem("B", {"protein": 30, "fat": 2, "carbs": 10})
        self.c = FoodItem("C", {"protein": 5, "fat": 1, "carbs": 30})

    def test_find_alternatives(self):
        mock_fc = MagicMock()
        mock_fc.searchDB.return_value = [self.a, self.b, self.c]

        # Your analyzer method name is find_alternatives(...)
        result = self.analyzer.find_alternatives(mock_fc, "test", limit=2)

        self.assertIn("highest_protein_per_cal", result)
        self.assertIn("lowest_fat_per_cal", result)
        self.assertIn("lowest_calorie", result)

        self.assertEqual(result["highest_protein_per_cal"][0].name, "B")
        self.assertEqual(result["lowest_fat_per_cal"][0].name, "C")


# ============================================================
# 4) Integration: Profile ↔ FoodItem Composition (Tidjani)
# ============================================================
class TestProfileFoodItemComposition(unittest.TestCase):

    def setUp(self):
        # Based on your traceback, Profile signature is Profile(weight, height)
        self.profile = Profile(180, 70)  # weight, height

        self.food = FoodItem("Apple", {"protein": 0.5, "fat": 0.2, "carbs": 25})

    def test_profile_is_not_fooditem(self):
        self.assertNotIsInstance(self.profile, FoodItem)

    def test_add_food_to_profile(self):
        # Support common Profile methods
        if hasattr(self.profile, "add_favorite"):
            self.profile.add_favorite(self.food)
        elif hasattr(self.profile, "add_to_favorites"):
            self.profile.add_to_favorites(self.food)
        elif hasattr(self.profile, "save_favorite"):
            self.profile.save_favorite(self.food)
        else:
            raise AttributeError("Profile must have an add method like add_favorite/add_to_favorites/save_favorite.")

        favorites = getattr(self.profile, "favorites", None)
        if favorites is None:
            favorites = getattr(self.profile, "_favorites", None)

        self.assertIsNotNone(favorites, "Profile must store favorites in favorites or _favorites.")
        self.assertIn(self.food, favorites)

    def test_fooditem_behavior_preserved(self):
        if hasattr(self.profile, "add_favorite"):
            self.profile.add_favorite(self.food)
        elif hasattr(self.profile, "add_to_favorites"):
            self.profile.add_to_favorites(self.food)
        elif hasattr(self.profile, "save_favorite"):
            self.profile.save_favorite(self.food)
        else:
            raise AttributeError("Profile must have an add method for favorites.")

        favorites = getattr(self.profile, "favorites", None)
        if favorites is None:
            favorites = getattr(self.profile, "_favorites", None)

        stored = favorites[0]
        self.assertEqual(stored.name, "Apple")
        self.assertGreater(stored.total_calories(), 0)


if __name__ == "__main__":
    unittest.main()
