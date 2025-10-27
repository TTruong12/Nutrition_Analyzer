

# Database_Manager - Theo
# 	Attributes
# API keys
# URLs


# get_food_item()
# def get_usda_food
# def get_openfoodfacts_food
# def prompt_key
# def set_key

import requests

class db_manager:
    """
    Manages GET calls to food central API
    Requires: requests library
    """

    def __init__(self, key = "DEMO_KEY"):
        self.__USDA_URL = "https://api.nal.usda.gov/fdc/v1" #URL for the food central database
        self.__usda_key = key  # Replace with your USDA key

        

    @property
    def USDA_URL(self):
        return self.__USDA_URL
    
    @property
    def usda_key(self):
        return self.__usda_key
    

    @usda_key.setter
    def usda_key(self, key = "DEMO_KEY"):
        """Sets api key to key parameter if valid key"""
        test_url = f"{USDA_URL}/food/0000000?api_key={key}"
        
        response = requests.get(test_url)
        if (response.status_code == 200):
            self.__usda_key = test_key
        else:
            print(f"Error. Status Code: {response.status_code}")


    def get_food_item(self, upc):
        """Given the universal product code, returns dictionary of details of that item"""
        url = f"{self.USDA_URL}/food/search?api_key={self.usda_key}&query={upc}"
        response = requests.get(url)

        if response.status_code == 200:
            food_data = response.json()
            return food_data
        else:
            print(f"Failed to retrieve data {response.status_code}")



    def prompt_key() -> str:
        """Prompts user for api key"""
        test_key = input("Enter USDA Food Central API key: ")
        return test_key

    
