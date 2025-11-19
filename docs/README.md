## Class Hierarchy

The nutrition model uses inheritance, polymorphism, and composition:

- `NutritionItem` (abstract base)
  - `FoodItem`: basic food with macro-based nutrients
  - `PackagedFood`: extends `FoodItem` to support servings and barcode
  - `Recipe`: a composite NutritionItem made of other NutritionItems

All subclasses implement:
- `total_calories()`: compute calories for the item
- `nutrient_summary()`: human-readable summary of nutrients

Example usage:

```python
from food_item import FoodItem, PackagedFood, Recipe, NutritionItem

items: list[NutritionItem] = [
    FoodItem("Apple", {"fat": 0, "protein": 0, "carbs": 25}),
    PackagedFood("Yogurt", {"fat": 3, "protein": 10, "carbs": 10}, servings=2),
]

recipe = Recipe("Oatmeal Bowl", ingredients=items)
print(recipe.total_calories())
