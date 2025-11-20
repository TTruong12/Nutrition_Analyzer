from db_manager import DBManager
import food_item
import requests

class FCManager(DBManager):

    def __init__(self, key = "DEMO_KEY"):
        super().__init__("https://api.nal.usda.gov/fdc/v1", key, "DEMO_KEY")
        
    def __repr__(self):
        return f'FC DB (url: "{self.url}")'

    @property
    def key(self):
        return self._key

    
    @DBManager.key.setter
    def key(self, key = ""):
        """Sets api key to key parameter if valid key. Resets key to DEMO_KEY if key is unspecified."""
        if key == "":
            key = self.prompt_key()
        print("Validating...")

        test_url = f"{self.url}/food/534358?api_key={key}" 
        
        response = requests.get(test_url)
        if (response.status_code == 200):
            self.__key = key
            print(f"Success. Status Code: {response.status_code}")
        else:
            print(f"Error. Status Code: {response.status_code}\nURL: {test_url}")

    def create_food_item(self, upc):
        """"""
        food_dict = self.get_item(upc)
        
        match food_dict["dataType"]:
            case "Foundation":
                return food_item.FoundationFood(food_dict["description"], food_dict["foodNutrients"], food_dict["scientificName"])
            case "Branded": 
                return food_item.BrandedFood(food_dict["brandOwner"], food_dict["foodNutrients"], food_dict["ingredients"])
            case _:
                return food_item.FoodItem(food_dict["description"], food_dict["foodNutrients"])
            
    def get_item(self, upc):
        """Given the universal product code, returns dictionary of details of that item"""
        request_url = f"{self.url}/food/{upc}?api_key={self.key}"
        print("Retrieving...")
        response = requests.get(request_url)

        if response.status_code == 200:
            food_data = response.json()
            return food_data
        else:
            print(f"Failed to retrieve data. Error {response.status_code}\nURL: {request_url}")
    
    def prompt_key(self) -> str:
        """Prompts user for api key or returns default key"""
        test_key = input("Enter API key (Press enter to use default): ")
        if test_key !="":
            return test_key
        else:
            return self.default_key
    
    def __repr__(self):
            return f"db_manager | URL: {self.url} API Key: {self.key}"   



