"""
food_item.py

Ben

Defines the FoodItem class representing food entry point
"""

class FoodItem:
    """Represents a single food item and its nutrient composition."""

    def __init__(self, name: str, nutrients: dict[str, float]):
        """
        Initialize a FoodItem object with parameter validation.


        Raises:
            ValueError: If name is invalid or nutrients is not a dictionary.
        """
        if not name or not isinstance(name, str):
            raise ValueError("Food name must be a non-empty string.")
        if not isinstance(nutrients, dict):
            raise ValueError("Nutrients must be a dictionary with numeric values.")

        self._name = name
        self._nutrients = nutrients

    # ---------- Properties ----------
    @property
    def name(self) -> str:
        """Get or set the food name."""
        return self._name

    @name.setter
    def name(self, new_name: str):
        if not new_name:
            raise ValueError("Name cannot be empty.")
        self._name = new_name

    @property
    def nutrients(self) -> dict[str, float]:
        """Get or set the nutrient composition."""
        return self._nutrients

    @nutrients.setter
    def nutrients(self, new_nutrients: dict[str, float]):
        if not isinstance(new_nutrients, dict):
            raise ValueError("Nutrients must be a dictionary.")
        self._nutrients = new_nutrients

    # ---------- Methods ----------
    def total_calories(self) -> float:
        """
        Calculate estimated total calories based on macronutrients.

        Returns:
            float: Estimated total calories.
        """
        fat = self._nutrients.get("fat", 0)
        protein = self._nutrients.get("protein", 0)
        carbs = self._nutrients.get("carbs", 0)
        return round((fat * 9) + (protein * 4) + (carbs * 4), 2)

    def nutrient_summary(self) -> str:
        """Return a formatted nutrient summary string."""
        return ", ".join(f"{k}: {v}g" for k, v in self._nutrients.items())

    def update_nutrient(self, key: str, value: float):
        """Update a single nutrient’s value."""
        if key not in self._nutrients:
            raise KeyError(f"{key} is not a valid nutrient.")
        if value < 0:
            raise ValueError("Nutrient values must be non-negative.")
        self._nutrients[key] = value

    # ---------- String Representations ----------
    def __str__(self):
        return f"{self._name}: {self.nutrient_summary()}"

    def __repr__(self):
        return f"FoodItem(Name={self._name!r}, Nutrients={self._nutrients!r})"
