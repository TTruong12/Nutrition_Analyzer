# --------------------------------------------------
# === Test #1 - Unit Test for scoring helpers ===
# --------------------------------------------------

import unittest
from food_item import FoodItem
from nutrition_analyzer import NutritionAnalyzer

class TestScoring(unittest.TestCase):

    def setUp(self):
        self.food = FoodItem("Test Food", {"protein": 10, "fat": 5, "carbs": 20})

    def test_protein_per_calorie(self):
        analyzer = NutritionAnalyzer({})
        score = analyzer.protein_per_calorie(self.food)
        expected = 10 / self.food.total_calories()
        self.assertAlmostEqual(score, expected, places=4)

    def test_fat_per_calorie(self):
        analyzer = NutritionAnalyzer({})
        score = analyzer.fat_per_calorie(self.food)
        expected = 5 / self.food.total_calories()
        self.assertAlmostEqual(score, expected, places=4)

# --------------------------------------------------
# === Test #2 - Unit Test for sorting functions ===
# --------------------------------------------------

class TestSorting(unittest.TestCase):

    def setUp(self):
        self.f1 = FoodItem("High P", {"protein": 20, "fat": 10, "carbs": 5})
        self.f2 = FoodItem("Medium P", {"protein": 10, "fat": 10, "carbs": 5})
        self.f3 = FoodItem("Low P", {"protein": 5, "fat": 10, "carbs": 5})
        self.analyzer = NutritionAnalyzer({})

    def test_sort_high_protein(self):
        result = self.analyzer.sort_high_protein([self.f3, self.f1, self.f2])
        self.assertEqual(result[0].name, "High P")
        self.assertEqual(result[-1].name, "Low P")

    def test_sort_low_fat(self):
        # all have same fat so order stable; just ensure no crash
        result = self.analyzer.sort_low_fat([self.f3, self.f1, self.f2])
        self.assertEqual(len(result), 3)

    def test_sort_low_calorie(self):
        result = self.analyzer.sort_low_calorie([self.f1, self.f2, self.f3])
        # lowest calories should be the one with lowest total nutrients
        self.assertEqual(result[0].name, "Low P")

# --------------------------------------------------
# === Test #3 - Integration test: search + alternatives ===
# --------------------------------------------------

from unittest.mock import MagicMock

class TestAlternativeIntegration(unittest.TestCase):

    def test_get_healthier_alternatives(self):
        # Mock FCManager
        mock_manager = MagicMock()

        f1 = FoodItem("A", {"protein": 10, "fat": 5, "carbs": 20})
        f2 = FoodItem("B", {"protein": 30, "fat": 2, "carbs": 10})
        f3 = FoodItem("C", {"protein": 5,  "fat": 1, "carbs": 30})
        
        mock_manager.searchDB.return_value = [f1, f2, f3]

        analyzer = NutritionAnalyzer({"food_name": "Test"})
        result = analyzer.get_healthier_alternatives(mock_manager, "test", limit=2)

        self.assertIn("highest_protein_per_cal", result)
        self.assertIn("lowest_fat_per_cal", result)
        self.assertIn("lowest_calorie", result)

        # Ensure correct sorting
        self.assertEqual(result["highest_protein_per_cal"][0].name, "B")
        self.assertEqual(result["lowest_fat_per_cal"][0].name, "C")
        self.assertEqual(result["lowest_calorie"][0].name, "C")



