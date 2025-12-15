# Nutrition Analyzer

Video Presentation: https://umd0-my.sharepoint.com/:v:/g/personal/aparkhie_umd_edu/IQDRiYfeoAkGQKuew_XXMPIxAXSrM_wtaNSLdzuVotiToYk?e=P5jWrE&nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D


An application that scans a food item and gives you information about the product and gives alternative recommendations.

Roles:

 Project Manager - Aneesh Parkhie
- Scheduling project meetings
- Keeps projects on timeline
- Resolves/Addresses team conflict

Lead Programmer - Tidjani Sow
- Delegating coding work
- Primary code reviewer
- Attends office hours for coding related issues

Quality Control - Theo Truong
- Tests Code
- Checks deliverables against the rubric/requirements
- Writes README’s/project documentation
- Oversees version control
- Secondary code reviewer

Liaison/Presenter - Benjamin Attota
- Submits project deliverables on time
- Primary speaker for final presentation

  
Domain Focus:
Health, Nutrition, and Food Informatics
The program operates in the intersection of nutrition science and data technology, specifically under dietary data retrieval and analysis.

Problem Statement:
Many consumers struggle to understand nutrition labels and compare food products in real time. Nutrient data is often scattered, inconsistently measured (metric vs imperial), or hidden behind barcodes that require manual lookup. This program sets out to solve this problem


Setup Instructions:
You will need to obtain your own API key by signing up at the USDA API portal (https://fdc.nal.usda.gov/api-key-signup).
Then, you will need to insert your own key into the USDA_API_KEY field.
There is a DEMO_KEY available, but it only works a limited amount of time.
Obtaining your own key is recommended.

Example use cases for functions:
- discovering healthier food option
- improving awareness of food intake 
- buying groceries for a healthier meal plan
- maximizing protein intake per calorie

Contribution Guidelines
Our team collaborates through GitHub using feature branches and pull requests. Each member focuses on specific areas: API integration, user interface, testing, and documentation. Code must follow programming standards, include clear comments, and run error-free. Before merging, at least one peer review is required. The main branch remains stable and is updated only after successful testing. Weekly check-ins ensure progress and task alignment. All commits must have descriptive messages and working examples. Each feature should be well-documented, tested with known barcodes, and contribute to a smooth, user-friendly nutrition analysis experience.

Design Decisions
Why Inheritance for Database Managers and Food Items?

Both database managers and food items share core attributes and behaviors, but differ in important specialization areas.

Database Managers (DBManager → FCManager)

Database managers share:

- API key handling
- Base URL storage
- External data retrieval concept
- Required interface methods (get_item, __repr__)

They differ in:

- API endpoints
- Request formats
- Response parsing
- Authentication behavior

Inheritance provides:

- Shared interface for all data sources
- Code reuse for API key and URL handling
- Polymorphic get_item behavior
- Clear “is-a” relationship
  (FCManager is a database manager)

Food Items (FoodItem → BrandedFoodItem)
Food items share:

- Name
- Nutrient data dictionary
- Calorie calculations
- Nutrient summaries:

They differ in:

- Branding information
- UPC/barcode
- Ingredient lists
- Packaging details

Inheritance provides:

- Shared nutrient logic from FoodItem
- Polymorphic string representation
- Cleaner specialization without duplicating code
- Clear “is-a” relationship
(BrandedFoodItem is a food item)

Why Composition for Profile and NutritionAnalyzer?

Profile manages:

- User-specific data (height/weight)
- Favorites list of foods

It is not:
- A type of food item
- A nutritional data source

Composition provides:

- Ability to store many FoodItem objects
- Flexible favorites management
- Separation between user and food domain models

NutritionAnalyzer operates on:

- Nutrient dictionaries
- Parsed API data

It is not:
- A food item itself
- A database manager

Composition provides:

- Flexibility to analyze any valid nutrient dict
- Ability to work with API data directly
- Clear separation between data storage and data analysis

Balancing Inheritance vs. Composition

Use Inheritance When:

- A clear “is-a” relationship exists

- Shared behavior belongs in a base class

- Polymorphic behavior is needed
(e.g., get_item dispatching to different APIs)

Use Composition When:

- A class has or manages other objects
- Coordinating multiple types
- The relationship is more important than the type
(e.g., a user having favorite foods)


```markdown
## Class Hierarchies

```mermaid
classDiagram
    class DBManager {
        - _url
        - _key
        - _default_key
        + prompt_key()
        + get_item()*
    }

    class FCManager {
        + get_item()
        + __repr__()
        + create_food_item()
    }

    DBManager <|-- FCManager

    class FoodItem {
        - _name
        - _nutrients
        + total_calories()
        + nutrient_summary()
        + update_nutrient()
    }

    class BrandedFoodItem {
        - _food_class = "Branded"
        - _brand_name
        - _ingredients
        - _upc
        + describe()
    }

    FoodItem <|-- BrandedFoodItem

    class Profile {
        - _weight
        - _height
        - _favorites : list[FoodItem]
        + add_favorite()
        + remove_favorite()
        + calculate_bmi()
    }

    Profile --> "0..*" FoodItem : favorites

* = abstract method from the DBManager interface.









