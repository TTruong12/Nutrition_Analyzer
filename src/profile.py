"""
profile.py

Ben

Sets the Profile class that represents a user’s data and favorite foods.

"""

from food_item import FoodItem

class Profile:
    """Represents a user profile with height, weight, and a collection of favorite foods."""

    def __init__(self, weight: float, height: float):
        """
        Initialize a Profile with weight and height validation.

        Args:
            weight (float): User weight in kilograms.
            height (float): User height in centimeters.

        Raises:
            ValueError: If weight or height are non-positive.
        """
        if weight <= 0:
            raise ValueError("Weight must be positive.")
        if height <= 0:
            raise ValueError("Height must be positive.")

        self._weight = weight
        self._height = height
        self._favorites: list[FoodItem] = []

    # ---------- Properties ----------
    @property
    def weight(self) -> float:
        return self._weight

    @weight.setter
    def weight(self, new_weight: float):
        if new_weight <= 0:
            raise ValueError("Weight must be positive.")
        self._weight = new_weight

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, new_height: float):
        if new_height <= 0:
            raise ValueError("Height must be positive.")
        self._height = new_height

    @property
    def favorites(self) -> list[FoodItem]:
        """Return a copy of the favorite foods list."""
        return list(self._favorites)

    # ---------- Methods ----------
    def add_favorite(self, food: FoodItem):
        """Add a FoodItem to favorites if it’s not already present."""
        if not isinstance(food, FoodItem):
            raise TypeError("Favorite must be a FoodItem instance.")
        if food not in self._favorites:
            self._favorites.append(food)

    def remove_favorite(self, food_name: str):
        """Remove a favorite food by its name (case-insensitive)."""
        self._favorites = [f for f in self._favorites if f.name.lower() != food_name.lower()]

    def manage_favorites(self):
        """Display all current favorites with nutrient summaries."""
        print("Favorites for user:")
        for item in self._favorites:
            print(f"- {item}")

    def create_and_manage_favorites(self, foods: list[FoodItem]):
        """
        Add multiple FoodItem objects to favorites and show them immediately.

        Args:
            foods (list[FoodItem]): List of FoodItem objects to add.
        """
        for food in foods:
            self.add_favorite(food)
        self.manage_favorites()

    def calculate_bmi(self) -> float:
        """Compute Body Mass Index (BMI) using metric units."""
        height_m = self._height / 100
        return round(self._weight / (height_m ** 2), 2)

    # ---------- String Representations ----------
    def __str__(self):
        return f"Profile(Weight={self._weight}kg, Height={self._height}cm, Favorites={len(self._favorites)})"

    def __repr__(self):
        return f"Profile(weight={self._weight!r}, height={self._height!r}, favorites={[f.name for f in self._favorites]!r})"
