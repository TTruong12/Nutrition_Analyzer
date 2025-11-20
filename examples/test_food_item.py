import pytest

from src.food_item import NutritionItem, FoodItem, PackagedFood, Recipe


def test_inheritance_hierarchy():
    """Ensure the inheritance hierarchy matches the design."""
    assert issubclass(FoodItem, NutritionItem)
    assert issubclass(PackagedFood, FoodItem)
    assert issubclass(Recipe, NutritionItem)


def test_fooditem_total_calories_macro_formula():
    """FoodItem uses the 9/4/4 macro formula."""
    item = FoodItem("Test Food", {"fat": 10, "protein": 5, "carbs": 20})
    # 10*9 + 5*4 + 20*4 = 90 + 20 + 80 = 190
    assert item.total_calories() == 190.0


def test_packagedfood_uses_super_and_servings():
    """
    PackagedFood should reuse FoodItem logic and multiply by servings.
    """
    base_nutrients = {"fat": 5, "protein": 5, "carbs": 10}
    # calories per serving: 5*9 + 5*4 + 10*4 = 45 + 20 + 40 = 105
    pf = PackagedFood("Yogurt", base_nutrients, servings=2)
    assert pf.total_calories() == 210.0  # 105 * 2

    # nutrient summary should mention servings
    summary = pf.nutrient_summary()
    assert "per serving" in summary
    assert "2" in summary


def test_recipe_composition_and_total_calories():
    """Recipe composes multiple NutritionItem objects and sums calories."""
    apple = FoodItem("Apple", {"fat": 0, "protein": 0, "carbs": 25})
    oats = FoodItem("Oats", {"fat": 4, "protein": 5, "carbs": 27})

    recipe = Recipe("Apple Oatmeal", [apple, oats])

    expected = apple.total_calories() + oats.total_calories()
    assert recipe.total_calories() == expected
    assert "ingredients" in recipe.nutrient_summary()


def test_polymorphic_behavior():
    """
    Polymorphism: all items share the same interface but behave differently.
    """
    apple = FoodItem("Apple", {"fat": 0, "protein": 0, "carbs": 25})
    yogurt = PackagedFood("Yogurt", {"fat": 3, "protein": 10, "carbs": 10}, servings=2)
    oats_recipe = Recipe("Oatmeal Bowl", [apple, yogurt])

    items: list[NutritionItem] = [apple, yogurt, oats_recipe]

    # All support total_calories() and nutrient_summary(), but results differ.
    calories = [item.total_calories() for item in items]
    assert all(c > 0 for c in calories)
    assert len(set(calories)) == 3  # all different

    summaries = [item.nutrient_summary() for item in items]
    assert len(summaries) == 3
    # Check that they are not all identical strings
    assert len(set(summaries)) == 3


def test_invalid_values_raise_errors():
    """Basic validation on names, nutrients, and servings."""
    with pytest.raises(ValueError):
        FoodItem("", {"fat": 0})

    with pytest.raises(ValueError):
        PackagedFood("Bad servings", {"fat": 1}, servings=0)

    item = FoodItem("Test", {"fat": 1})
    with pytest.raises(KeyError):
        item.update_nutrient("protein", 10)  # not in dict

    with pytest.raises(ValueError):
        item.update_nutrient("fat", -1)
