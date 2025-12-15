from db_manager import DBManager
from food_item import BrandedFoodItem, FoundationFoodItem, FoodItem
import requests
from dataclasses import dataclass

import nltk




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
                return FoundationFoodItem(food_data["description"], food_data["foodNutrients"], food_data["scientificName"])
            case "Branded": 
                # print(food_data['foodNutrients'])
                return BrandedFoodItem(food_data["description"], food_data["brandOwner"], food_data["foodNutrients"], food_data["ingredients"], food_data["gtinUpc"])
            case _:
                return FoodItem(food_data["description"], food_data["foodNutrients"])
            

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
                request_url = f"{self.url}/foods/search?api_key={self.key}&query={query}" #gtinUPC%3A%20
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
                # print(food_data['foods'][0]['description'])
                return self.create_food_item(food_data['foods'][0])
            elif food_data['totalHits'] > 1:
                foodlist = []
                for i in range(len(food_data['foods'])):
                    foodlist.append(food_data['foods'][i])
                #print(food_data)

                return self.get_relevant(query, foodlist)
        else:
            print(f"Failed to retrieve data. Error {response.status_code}\nURL: {request_url}")
            # print(response.text)
        


    def get_relevant(self, query, results):
        """Returns 100 most relevant using TF-IDF for the list of food dictionaries"""
        docs = []
        i = 0
        limit = 3
        for val in results: #adds all results to a list as a string of relevant text 
            
            # if i>limit: #limiting number of search results processed
            #     break
            docRepr = ""
            if 'description' in val:
                docRepr += str(val['description'])
            if 'ingredients' in val:
                docRepr += str(val['ingredients'])
            if 'brandedFoodCategory' in val:
                docRepr +=str(val['brandedFoodCategory'])
            if 'brandOwner' in val:
                docRepr += str(val['brandOwner'])
            # print(f"$$$ {docRepr}")
            docs.append(docRepr)
            results[i]['relScore'] = self.computeTFIDF(docRepr,query)
            # print(results[i]['relScore'])
            i +=1
        # for val in results:
        # print(val.keys())
        results = sorted(results, key = lambda x: x.get('relScore', 0))
        # print(results[0].get('relScore'))
        # print(results[-1].get('relScore'))
        
        ranked = []
        i = 0
        for val in results:
            if i >= 100:
                break
            # print("Score: " + str(val['relScore']))
            temp_food = self.create_food_item(val)
            # print("Created: " + str(temp_food))
            ranked.append(temp_food)
            i += 1


        return ranked

        
        
            


    def tokenize(self, text:str):
        stop_sym = [".",",","(",")"]
        stop_words = ["the", "in", "a"]
        for sym in stop_sym: 
            text.replace(sym , " ")
        tokens = text.lower().split()

        
        filtered_tokens = [word for word in tokens if word not in stop_words]
        
        filteredText = ""
        for val in filtered_tokens:
            filteredText +=val + " "
        # print(filteredText)
        return filteredText
    
    def computeTFIDF(self, text, query:str):
        """Returns term frequency of text"""
        # query = self.tokenize(query)
        qwords = query.split()

        text = self.tokenize(text)
        twords = text.split()
        
        tfDict = {}
        for val in twords:
            if val in tfDict:
                tfDict[val] +=1
            else:
                tfDict[val] = 0
        
        tfidfs = {}
        for val in qwords:
            if val in tfDict:
                tfidfs[val] = tfDict[val]/len(text)
        
        score = 0
        for val in tfidfs:
            score += tfidfs[val]
        return score

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
# x = FCManager("DEMO_KEY")
# test_q = x.searchDB("Kit Kat",0)
# for i in test_q:
#     print(i)

# x = FCManager()
# results = x.searchDB("apple",0)
# for val in results:
#     print(val)
