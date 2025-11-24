# Nutrition Analyzer
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
(as of now this program only works fully in Google Colab)
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











