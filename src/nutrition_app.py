from foodcentral_manager import FCManager
from nutrition_analyzer import NutritionAnalyzer
from profile import Profile
from food_item import FoodItem

import pickle
import json
from pathlib import Path 

class NutritionApp:
    """
    Main application controller for nutrition analysis and user interaction.
    Coordinates database access, nutrition analysis, and visual display.
    """

    def __init__(self):
        self.fc_db: FCManager
        self.analyzer: NutritionAnalyzer
        self.profile: Profile
        
        
    def create_user_profile(self):
        w = float(input("Enter your weight (kg): ").strip())
        h = float(input("Enter your height (cm): ").strip())
        self.profile = Profile(w, h)
        print(f"Profile created. BMI: {self.profile.calculate_bmi()}")
        #profile.create_favorites #implement data persistance


    
    def start_up(self):
        print("Loading...")

        self.fc_db = FCManager()
        p = Path("profile.json")

        if p.exists():
            print("Loading profile...")
            with open('profile.json', 'r') as file:
                data = json.load(file)
                self.profile = Profile(data['weight'], data['height'])
                self.profile.create_favorites(data['favorites'])
        else:
            self.create_user_profile() #if first session
            with open('profile.json', 'w') as file:
                data = {'weight': self.profile.weight, 'height': self.profile.height, 'favorites': []}
                json.dump(data, file)


        self.analyzer = NutritionAnalyzer()

        self.fc_db.prompt_key()
        
    def run(self):
        print("Welcome to the Nutrition App")
        self.start_up()
        while True:
            choice = input("1) Search food  2) Manage Profile 3) Quit: ").strip()
            if choice == "1":
                query = input("Enter food name or UPC: ").strip()
                if query.isnumeric():
                    print("UPC Search")
                    result = self.fc_db.searchDB(query,1)
                    
                    # print(type(result))
                    if result is None:
                        print("Not found in database")
                    else:
                        print(f"Food item found: {result}")
                        self.compare_menu(result)
                        # print("Searching for alternatives...")
                        # related = self.fc_db.searchDB(result.name,1)
                        # alters = self.analyzer.get_healthier_alternatives(related)
                        # self.display_alter(alters)
                else:
                    print("Keyword Search")
                    result = self.fc_db.searchDB(query) 
                    if type(result) == list:
                        print("Search results")
                        for i, val in enumerate(result):
                            if i > 4:
                                break
                            print(f"{i}.) {val}")
                        select = input("Enter number of item (anything else to cancel)")
                        if type(select.strip().isnumeric):
                            select = int(select)
                            if select > 5 or select < 1:
                                break
                            else:
                                pass
                    else:
                        pass

                                

                
            
            
            elif choice == "2":
                self.profile_menu()
            
            
            elif choice == "3":
                print("Shutting down.")
                break
            else:
                print("Invalid option.")
    def compare_menu(self, fooditem):
        upc = input("Enter UPC of second food item (Enter to cancel): ")
        if upc == "":
            print("Cancelled")
            return
        else: 
            fooditem2 = self.fc_db.searchDB(upc,1)
            self.display_comparison(fooditem,fooditem2)
            return
    def display_comparison(self, item1, item2):
        print(f"         {item1.name} | {item1.name} ")
       
        print(f"calories {item1.calorie} | {item2.calorie}")
        print(f"carbs    {item1.carb} | {item2.carb}")
        print(f"protein  {item1.protein} | {item2.protein}")
        print(f"fat      {item1.fat} | {item2.fat}")
        


    def display_alter(self, alters):
        """Takes dictionary of alternative food items and formats/prints message"""
        print(f"Higher protein option: {alters['protein']}\n ({alters['protein'].protein})")
        print(f"Lower fat option: {alters['calorie']}\n ({alters['calorie'].calorie})")
        print(f"Lower carb option: {alters['carb']}\n ({alters['carb'].carb})")


    def profile_menu(self):
        profile = self.profile
        fc_db = self.fc_db
        print(profile)
        while True:
            choice = input("1) Add Favorite 2) Remove Favorites 3) Display Profile 4) Quit: ").strip()
            match choice:
                case "1":
                    upc = input("Enter UPC of the food item: ") 
                    fav_select = type(fc_db.searchDB(upc))
                    if  fav_select == FoodItem:
                        profile.add_favorite(fav_select)
                        with open("profile.json", 'r+') as file:
                            data = json.load(file)
                            data['favorites'].append(fav_select)
                            json.dump(data,file)
                case "2":
                    profile.display_favorites()
                    index = int(input(f"Enter a number (1-{len(profile.favorites)}) to select the food to remove"))-1
                    profile.remove_favorite(index)

                    with open("profile.json", 'r+') as file:
                            data = json.load(file)
                            if 'favorites' in data:
                                data['favorites'] = profile.favorites
                            json.dump(data,file)
                case "3":
                    print(profile)
                case "4":
                    return

    def __str__(self):
        return f"NutritionApp(Profile={self._profile})"

    def __repr__(self):
        return f"NutritionApp(db={self._db!r}, profile={self._profile!r})"





