db_manager: contains functions and data about the API(s) used in the application
profile: contains data about the user (health information would be used to make personalized recommendations in future versions) 
food_item: contains info about a food item in order to have offline/easier access to the food item's information. used to store info on user's favorited items.
nutrition_analyzer: contains functions to calculate graphics and evaluations from the data retrieved by db_manager (and potentially data from profile) 
graphics: contains functions to visualize nutritional data
nutrition_app: contains the overall control flow of the application and how the other classes are implemented 
