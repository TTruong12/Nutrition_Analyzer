"""
food_item.py
Classes representing food entries with nutrient data.
"""

from __future__ import annotations
from typing import Dict, List



class FoodItem():
    """Represents a single food item and its nutrient composition."""

    def __init__(self, name: str, nutrients: Dict):
        """
        Initialize a FoodItem object with parameter validation.

        Args:
            name (str): Name of the food item.
            nutrients (dict[str, float]): Nutrient composition,
                e.g. {"fat": 10, "protein": 5, "carbs": 20}.
        """
        self._name = name
        self._nutrients = nutrients

    @property
    def name(self):
        return self._name

    @property
    def nutrients(self) -> Dict[str, float]:
        """Get or set the nutrient composition."""
        return self._nutrients

    @nutrients.setter
    def nutrients(self, new_nutrients: Dict[str, float]) -> None:
        if not isinstance(new_nutrients, dict):
            raise ValueError("Nutrients must be a dictionary.")
        self._nutrients = new_nutrients

    
    # def total_calories(self) -> float:
    #     """
    #     Calculate estimated total calories based on macronutrients.
    #     Uses Project 1 formula logic: 9 kcal/g fat, 4 kcal/g protein, 4 kcal/g carbs.

    #     Returns:
    #         float: Estimated total calories.
    #     """
    #     fat = self._nutrients.get("fat", 0)
    #     protein = self._nutrients.get("protein", 0)
    #     carbs = self._nutrients.get("carbs", 0)
    #     return round((fat * 9) + (protein * 4) + (carbs * 4), 2)

    def nutrient_summary(self) -> str:
        """Return a formatted nutrient summary string."""
        if not self._nutrients:
            return "no nutrient data"
        return ", ".join(f"{k}: {v}g" for k, v in self._nutrients.items())

    # def update_nutrient(self, key: str, value: float) -> None:
    #     """Update a single nutrient’s value."""
    #     if key not in self._nutrients:
    #         raise KeyError(f"{key} is not a valid nutrient.")
    #     if value < 0:
    #         raise ValueError("Nutrient values must be non-negative.")
    #     self._nutrients[key] = value

    def __repr__(self) -> str:
        return f"FoodItem(name={self.name!r}, nutrients={self._nutrients!r})"



# Derived class: PackagedFood


# class PackagedFood(FoodItem):
#     """
#     Represents a packaged food item with servings.

#     Inherits nutrient logic from FoodItem but allows multiple servings
#     and optional barcode information.
#     """

#     def __init__(
#         self,
#         name: str,
#         nutrients_per_serving: Dict[str, float],
#         servings: float = 1.0,
#         barcode: str | None = None,
#     ):
#         super().__init__(name=name, nutrients=nutrients_per_serving)
#         if servings <= 0:
#             raise ValueError("Servings must be positive.")
#         self._servings = servings
#         self.barcode = barcode

#     @property
#     def servings(self) -> float:
#         return self._servings

#     @servings.setter
#     def servings(self, value: float) -> None:
#         if value <= 0:
#             raise ValueError("Servings must be positive.")
#         self._servings = value

#     def total_calories(self) -> float:
#         """
#         Total calories = calories per serving * number of servings.
#         Reuses FoodItem.total_calories() via super().
#         """
#         per_serving = super().total_calories()
#         return round(per_serving * self._servings, 2)

#     def nutrient_summary(self) -> str:
#         base = super().nutrient_summary()
#         return f"{base} (per serving) x {self._servings} serving(s)"

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
        scientific_name: str
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



class BrandedFoodItem(FoodItem):

    def __init__(self, name, brand_name, nutrients, ingredients, upc: str):
        super().__init__(name=name, nutrients=nutrients)
        self._food_class = "Branded"
        self._brand_name = brand_name.strip()

        # print(type(nutrients))
        for val in nutrients:
            if val["nutrientName"] == 'Protein':
                self._protein = val['value']    
            if val["nutrientName"] == 'Total lipid (fat)':
                self._fat = val["value"]
            if val["nutrientName"] == 'Carbohydrate, by difference':
                self._carb = val["value"]
            if val["nutrientName"] == "Energy":
                self._calorie = val["value"]
        
        self._ingredients = [i.strip() for i in ingredients]
        self._upc = upc


    @property
    def protein(self):
        return self._protein

    @property
    def carb(self):
        return self._carb

    @property
    def fat(self):
        return self._fat
    
    @property
    def calorie(self):
        return self._calorie
    

    
    @property
    def food_class(self) -> str:
        return self._food_class

    @property
    def brand_name(self) -> str:
        return self._brand_name

    @brand_name.setter
    def brand_name(self, value: str) -> None:
        value = value.strip()
        if not value:
            raise ValueError("Brand name cannot be empty.")
        self._brand_name = value

    @property
    def ingredients(self) -> List[str]:
        return list(self._ingredients)

    @ingredients.setter
    def ingredients(self, value: List[str]) -> None:
        if not isinstance(value, list):
            raise TypeError("Ingredients must be a list of strings.")
        self._ingredients = [str(i).strip() for i in value]

    @property
    def upc(self) -> str:
        return self._upc

    @upc.setter
    def upc(self, value: str) -> None:
        value = value.strip()
        if not value:
            raise ValueError("UPC cannot be empty.")
        self._upc = value

    def describe(self) -> str:
        return f"{self.brand_name} {self.name} [{self.food_class}] (UPC: {self.upc})"

    def __str__(self) -> str:
        return f"{self.brand_name} {self.name} ({self.food_class})"

    def __repr__(self) -> str:
        return (
            f"BrandedFoodItem(name={self.name!r}, brand_name={self.brand_name!r}, "
            f"upc={self.upc!r}, nutrients={self.nutrients!r})"
        )
