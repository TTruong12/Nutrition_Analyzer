from db_manager import DBManager
import food_item 
import requests
from dataclasses import dataclass



class FCManager(DBManager):
    """
    Manages GET calls to USDA's Food Central Database
    """
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

    def create_food_item(self, food_data):
        """creates a FoodItem object from food central database"""
        if type(food_data) != dict:
            print('Invalid food data')
            return

        
        match food_data["dataType"]:
            case "Foundation":
                return food_item.FoundationFood(food_data["description"], food_data["foodNutrients"], food_data["scientificName"])
            case "Branded": 
                return food_item.BrandedFood(food_data["description"], food_data["brandOwner"], food_data["foodNutrients"], food_data["ingredients"], food_data["gtinUpc"])
            case _:
                return food_item.FoodItem(food_data["description"], food_data["foodNutrients"])
            
    def get_item(self, fdcID):
        """Given the Food Central Database ID, returns dictionary of details of that item"""
        request_url = f"{self.url}/food/{fdcID}?api_key={self.key}"
        print("Retrieving...")
        response = requests.get(request_url)

        if response.status_code == 200:
            food_data = response.json()
            return food_data
        else:
            print(f"Failed to retrieve data. Error {response.status_code}\nURL: {request_url}")
    

    def searchDB(self, query:str, key = 0):
        """Finds food items in FCDB that match search conditions
        key = 0: Searches by keyword
        key = 1: Searches by UPC
        
        Returns food item object if one matching search result
        and returns list of food item objects if multiple matches 
        """
        request_url = ""

        if key == 0:
            query = query.strip().replace(" ", "%20")
            request_url = f"{self.url}/foods/search?api_key={self.key}&query={query}?"
        elif key == 1:
            query = query.strip()
            if query.isnumeric():
                request_url = f"{self.url}/foods/search?api_key={self.key}&query=gtinUPC%3A%20{query}"
            else:
                print("Invalid UPC")
                return
        print("Retrieving...")
        response = requests.get(request_url)

        if response.status_code == 200:
            food_data = response.json()

            if food_data['totalHits'] == 0:
                print("Food item not found")
            elif food_data['totalHits'] == 1:
                return food_item(food_data['foods']['fdcID'])
            elif food_data['totalHits'] > 1:
                foodlist = []
                for i in range(len(food_data['foods'])):
                    foodlist.append(self.create_food_item(food_data['foods'][i]))
                return foodlist
        else:
            print(f"Failed to retrieve data. Error {response.status_code}\nURL: {request_url}")
            # print(response.text)
        
    def prompt_key(self) -> str:
        """Prompts user for api key or returns default key"""
        test_key = input("Enter API key (Press enter to use default): ")
        if test_key !="":
            return test_key
        else:
            return self.default_key
    
    def __repr__(self):
            return f"db_manager | URL: {self.url} API Key: {self.key}"   



#test
x = FCManager("of0bq8jn7Kmnfr7hsoTSw9lC3Guu7YYa7YcQ9IFX")
test_q = x.searchDB("Kit Kat",0)
for i in test_q:
    print(i)