

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

    __USDA_URL = "https://api.nal.usda.gov/fdc/v1" #URL for the food central database
    __usda_key = "DEMO_KEY"  # Replace with your USDA key

        

    @classmethod
    def USDA_URL(cls):
        return cls.__USDA_URL
    
    @classmethod
    def usda_key(cls):
        return cls.__usda_key
    

    @classmethod
    def usda_key(cls, key = "DEMO_KEY"):
        """Sets api key to key parameter if valid key"""
        print("Validating...")
        test_url = f"{cls.__USDA_URL}/food/534358?api_key={key}" 
        
        response = requests.get(test_url)
        if (response.status_code == 200):
            cls.__usda_key = key
            print(f"Success. Status Code: {response.status_code}")
        else:
            print(f"Error. Status Code: {response.status_code}\nURL: {test_url}")


    @classmethod
    def get_food_item(cls, upc):
        """Given the universal product code, returns dictionary of details of that item"""
        url = f"{cls.__USDA_URL}/food/{upc}?api_key={cls.__usda_key}"

        print("Retrieving...")
        
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

#tests
#db_manager.usda_key(db_manager.prompt_key())
#print(db_manager.get_food_item(534358))

#print(db_manager.USDA_URL())
