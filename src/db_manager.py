

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
    def __init__(self, url, key, default_key):
        self.__url = url
        self.__key = key
        self.__default_key = default_key 

    @classmethod
    def foodcentral(cls, key = "DEMO_KEY"):
        return cls("https://api.nal.usda.gov/fdc/v1", key, "DEMO_KEY")

    def __repr__(self):
        return f"db_manager | URL: {self.url} API Key: {self.key}"    
    

    @property
    def url(self):
        return self.__url
    
    @property
    def key(self):
        return self.__key
    
    @property
    def default_key(self):
        return self.__default_key

    @key.setter
    def key(self, key = "DEMO_KEY"):
        """Sets api key to key parameter if valid key. Resets key to DEMO_KEY if key is unspecified."""
        if key == "DEMO_KEY" or key == "":
            key = self.prompt_key()
        print("Validating...")

        test_url = f"{self.url}/food/534358?api_key={key}" 
        
        response = requests.get(test_url)
        if (response.status_code == 200):
            self.__key = key
            print(f"Success. Status Code: {response.status_code}")
        else:
            print(f"Error. Status Code: {response.status_code}\nURL: {test_url}")


    
    def get_food_item(self, upc):
        """Given the universal product code, returns dictionary of details of that item"""
        request_url = f"{self.url}/food/{upc}?api_key={self.key}"
        print("Retrieving...")
        response = requests.get(request_url)

        if response.status_code == 200:
            food_data = response.json()
            return food_data
        else:
            print(f"Failed to retrieve data {response.status_code}\nURL: {request_url}")


    
    def prompt_key(self) -> str:
        """Prompts user for api key"""
        test_key = input("Enter API key (Press enter to use default): ")
        if test_key !="":
            return test_key
        else:
            return self.default_key

#tests
fc_db = db_manager.foodcentral()
print(repr(fc_db))

#print(fc_db.url)
#print(fc_db.get_food_item(534358))

