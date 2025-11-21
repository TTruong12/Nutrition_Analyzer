"""
food_item.py

Classes representing food entries with nutrient data.

This extends the original FoodItem from Project 2 to use:
- An abstract base class using intheritance, polymorphism, and composition.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List



# Abstract base class


class NutritionItem(ABC):
    """
    Abstract base class for anything that has a name and calories.

    Subclasses must implement:
    - total_calories()
    - nutrient_summary()
    """

    def __init__(self, name: str):
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string.")
        self._name = name

    @property
    def name(self) -> str:
        """Get or set the item name."""
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        if not new_name:
            raise ValueError("Name cannot be empty.")
        self._name = new_name

    @abstractmethod
    def total_calories(self) -> float:
        """
        Return the total calories for this item.
        Must be implemented by subclasses.
        """
        raise NotImplementedError

    @abstractmethod
    def nutrient_summary(self) -> str:
        """
        Return a human-readable nutrient summary.
        Must be implemented by subclasses.
        """
        raise NotImplementedError

    def __str__(self) -> str:
        return f"{self.name}: {self.nutrient_summary()}"

    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        return f"{cls_name}(name={self.name!r})"



# Base concrete class 


class FoodItem(NutritionItem):
    """Represents a single food item and its nutrient composition."""

    def __init__(self, name: str, nutrients: Dict[str, float]):
        """
        Initialize a FoodItem object with parameter validation.

        Args:
            name (str): Name of the food item.
            nutrients (dict[str, float]): Nutrient composition,
                e.g. {"fat": 10, "protein": 5, "carbs": 20}.

        Raises:
            ValueError: If name is invalid or nutrients is not a dictionary.
        """
        super().__init__(name=name)

        if not isinstance(nutrients, dict):
            raise ValueError("Nutrients must be a dictionary with numeric values.")

        self._nutrients: Dict[str, float] = nutrients

    @property
    def nutrients(self) -> Dict[str, float]:
        """Get or set the nutrient composition."""
        return self._nutrients

    @nutrients.setter
    def nutrients(self, new_nutrients: Dict[str, float]) -> None:
        if not isinstance(new_nutrients, dict):
            raise ValueError("Nutrients must be a dictionary.")
        self._nutrients = new_nutrients

    def total_calories(self) -> float:
        """
        Calculate estimated total calories based on macronutrients.
        Uses Project 1 formula logic: 9 kcal/g fat, 4 kcal/g protein, 4 kcal/g carbs.

        Returns:
            float: Estimated total calories.
        """
        fat = self._nutrients.get("fat", 0)
        protein = self._nutrients.get("protein", 0)
        carbs = self._nutrients.get("carbs", 0)
        return round((fat * 9) + (protein * 4) + (carbs * 4), 2)

    def nutrient_summary(self) -> str:
        """Return a formatted nutrient summary string."""
        if not self._nutrients:
            return "no nutrient data"
        return ", ".join(f"{k}: {v}g" for k, v in self._nutrients.items())

    def update_nutrient(self, key: str, value: float) -> None:
        """Update a single nutrient’s value."""
        if key not in self._nutrients:
            raise KeyError(f"{key} is not a valid nutrient.")
        if value < 0:
            raise ValueError("Nutrient values must be non-negative.")
        self._nutrients[key] = value

    def __repr__(self) -> str:
        return f"FoodItem(name={self.name!r}, nutrients={self._nutrients!r})"



# Derived class: PackagedFood


class PackagedFood(FoodItem):
    """
    Represents a packaged food item with servings.

    Inherits nutrient logic from FoodItem but allows multiple servings
    and optional barcode information.
    """

    def __init__(
        self,
        name: str,
        nutrients_per_serving: Dict[str, float],
        servings: float = 1.0,
        barcode: str | None = None,
    ):
        super().__init__(name=name, nutrients=nutrients_per_serving)
        if servings <= 0:
            raise ValueError("Servings must be positive.")
        self._servings = servings
        self.barcode = barcode

    @property
    def servings(self) -> float:
        return self._servings

    @servings.setter
    def servings(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Servings must be positive.")
        self._servings = value

    def total_calories(self) -> float:
        """
        Total calories = calories per serving * number of servings.
        Reuses FoodItem.total_calories() via super().
        """
        per_serving = super().total_calories()
        return round(per_serving * self._servings, 2)

    def nutrient_summary(self) -> str:
        base = super().nutrient_summary()
        return f"{base} (per serving) x {self._servings} serving(s)"

class FoundationFoodItem(FoodItem):
    """
    Represents a USDA foundational food item.

    Adds subclass-specific attributes:
    - common_name: everyday food name used by consumers
    - scientific_name: formal botanical/biological name

    Also sets:
    - foodClass = "Foundational"
    """

    def __init__(
        self,
        name: str,
        nutrients: Dict[str, float],
        common_name: str,
        scientific_name: str,
    ):
        # Call FoodItem initializer (handles name + nutrients validation)
        super().__init__(name=name, nutrients=nutrients)

        # Subclass-specific validation
        if not common_name:
            raise ValueError("Common name cannot be empty.")
        if not scientific_name:
            raise ValueError("Scientific name cannot be empty.")

        # New attributes
        self.common_name = common_name
        self.scientific_name = scientific_name

        # Fixed subclass attribute
        self.foodClass = "Foundational"

    def nutrient_summary(self) -> str:
        """
        Override nutrient_summary() to include subclass information.
        """
        base = super().nutrient_summary()
        return f"{base} | Common: {self.common_name}, Scientific: {self.scientific_name}"


# Derived class + composition


class Recipe(NutritionItem):
    """
    A recipe is a NutritionItem composed of other NutritionItem ingredients.

    This demonstrates both:
    - Inheritance 
    - Composition 
    """

    def __init__(self, name: str, ingredients: List[NutritionItem] | None = None):
        super().__init__(name=name)
        self._ingredients: List[NutritionItem] = ingredients or []

    @property
    def ingredients(self) -> List[NutritionItem]:
        return list(self._ingredients)

    def add_ingredient(self, item: NutritionItem) -> None:
        """Add a NutritionItem (FoodItem, PackagedFood, another Recipe, etc.)"""
        self._ingredients.append(item)

    def total_calories(self) -> float:
        return round(sum(item.total_calories() for item in self._ingredients), 2)

    def nutrient_summary(self) -> str:
        if not self._ingredients:
            return "no ingredients"
        inner = "; ".join(item.nutrient_summary() for item in self._ingredients)
        return f"ingredients: [{inner}]"

    def __repr__(self) -> str:
        return f"Recipe(name={self.name!r}, ingredients={len(self._ingredients)} items)"
