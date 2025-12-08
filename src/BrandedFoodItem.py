from food_item import FoodItem
from typing import Dict, List

class BrandedFoodItem(FoodItem):

    def __init__(
        self,
        name: str,
        nutrients: Dict[str, float],
        brand_name: str,
        ingredients: List[str],
        upc: str
    ):
        super().__init__(name=name, nutrients=nutrients)
        self._food_class = "Branded"
        self._brand_name = brand_name.strip()
        self._ingredients = [i.strip() for i in ingredients]
        self._upc = upc.strip()

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
