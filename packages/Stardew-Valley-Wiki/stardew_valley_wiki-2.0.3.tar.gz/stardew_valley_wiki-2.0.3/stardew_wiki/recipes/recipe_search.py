import pandas as pd

class RecipeNotFoundError(Exception):
    """Custom exception raised when a recipe cannot be found"""
    def __init__(self, recipe_name):
        self.recipe_name = recipe_name
        self.message = f"Recipe '{recipe_name}' not found in the database"
        super().__init__(self.message)


# Functions for recipe_search
def list_all_recipes(recipes_df):
    """Lists all recipe names from the Recipes data."""
    try:
        # Check if the dataframe is empty
        if recipes_df.empty:
            print("No recipes available.")
            return
        
        # Check if the column exists
        if 'name_recipe' not in recipes_df.columns:
            raise KeyError("Column 'name_recipe' not found in the dataframe.")
        
        # Extract and print recipes
        recipes = recipes_df['name_recipe'].tolist()
        print("Available Recipes:")
        for recipe in recipes:
            print(f"- {recipe}")
    
    except AttributeError:
        print("Error: Input is not a valid pandas DataFrame.")
    except KeyError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
def search_recipe_by_name(recipes_df):
    """Search for a recipe with exception handling"""
    try:
        name = input("Enter the name of the recipe to search: ").strip()
        if not isinstance(recipes_df, pd.DataFrame):
            raise TypeError("Invalid data format: recipes_df must be a pandas DataFrame")
            
        recipe = recipes_df[recipes_df['name_recipe'].str.contains(name, case=False, na=False)]
        if recipe.empty:
            raise RecipeNotFoundError(name)
            
        print(f"Recipe: {recipe.iloc[0]['name_recipe']}")
        print(f"Ingredients: {recipe.iloc[0]['ingredients']}")
    
    except RecipeNotFoundError as e:
        print(f"Error: {e}")
    except TypeError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def ingredient_details(crops_df, animals_df):
    """Get ingredient details with exception handling"""
    try:
        if not isinstance(crops_df, pd.DataFrame) or not isinstance(animals_df, pd.DataFrame):
            raise TypeError("Invalid data format: both crops_df and animals_df must be pandas DataFrames")
            
        while True:
            user_input = input("Enter the ingredient name to see details (or type 'STOP' to quit): ").strip()
            if user_input.lower() == 'stop':
                break
            
            if not user_input:
                raise ValueError("Ingredient name cannot be empty")

            # Search in crops (name_crop and craft_crop)
            crop_detail = crops_df[
                (crops_df['name_crop'] == user_input) | (crops_df['craft_crop'] == user_input)
            ]
            
            # Search in animals (product_animal)
            animal_detail = animals_df[animals_df['product_animal'] == user_input]

            if crop_detail.empty and animal_detail.empty:
                print("\nIngredient not found in Crops or Animals.")
                continue

            # Display crop details if found
            if not crop_detail.empty:
                print("\nIngredient found in Crops:")
                for index, row in crop_detail.iterrows():
                    print(f"Name: {row['name_crop']}")
                    print(f"Craft Name: {row.get('craft_crop', 'N/A')}")
                    print(f"Season: {row['season']}")
                    print(f"Growth Time: {row['growth_crop']} days")
                    print(f"Regrowth Time: {row.get('regrowth_crop', 'N/A')} days")
                    print(f"Price: {row['crop_price']}")
                    print(f"Craft Price: {row.get('craft_crop_price', 'N/A')}")
                    print("-" * 40)

            # Display animal details if found
            if not animal_detail.empty:
                print("\nIngredient found in Animals:")
                for index, row in animal_detail.iterrows():
                    print(f"Animal: {row['name_animal']}")
                    print(f"Type: {row['type']}")
                    print(f"Growth Time: {row['growth_animal']}")
                    print(f"Product: {row['product_animal']}")
                    print(f"Product Price: {row['product_animal_price']}")
                    print(f"Artisan Product: {row.get('artisan_animal', 'N/A')}")
                    print(f"Artisan Product Price: {row.get('artisan_animal_price', 'N/A')}")
                    print("-" * 40)
                    
    except TypeError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
