import pandas as pd

class RecipeNotFoundError(Exception):
    """Custom exception raised when a recipe cannot be found"""
    def __init__(self, recipe_name):
        self.recipe_name = recipe_name
        self.message = f"Recipe '{recipe_name}' not found in the database"
        super().__init__(self.message)


def list_all_ingredients(recipes_df):
    """
    Lists all unique ingredients from the 'ingredients' column.
    Removes parentheses and numbers, ensuring unique ingredient names.
    """
    try:
        # Check if the dataframe is empty
        if recipes_df.empty:
            print("No ingredients available.")
            return []
        
        # Check if the 'ingredients' column exists
        if 'ingredients' not in recipes_df.columns:
            raise KeyError("Column 'ingredients' not found in the dataframe.")
        
        # Step 1: Split the ingredients into individual items
        ingredients = (
            recipes_df['ingredients']
            .str.split(',')  # Split by comma
            .explode()  # Expand into individual rows
            .str.strip()  # Remove extra spaces
            .dropna()  # Drop any NaN values
        )
        
        # Step 2: Remove text inside parentheses (e.g., '(1)') using regex
        clean_ingredients = (
            ingredients.str.replace(r"\(.*?\)", "", regex=True)  # Remove content in parentheses
            .str.replace(r"\d+", "", regex=True)  # Remove digits
            .str.strip()  # Strip spaces again after cleanup
            .unique()  # Get unique ingredients
        )
        
        # Step 3: Print each ingredient line by line
        print("\nUnique Ingredients:")
        for ingredient in sorted(clean_ingredients):  # Sort alphabetically for better readability
            print(f"- {ingredient}")
        
        return clean_ingredients
    
    except AttributeError:
        print("Error: Input is not a valid pandas DataFrame.")
        return []
    except KeyError as e:
        print(f"Error: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

def search_recipes_by_ingredients(recipes_df):
    """Finds recipes that use the provided ingredients."""
    try:
        # Check if the dataframe is empty
        if recipes_df.empty:
            print("No recipes available.")
            return
        
        # Check if required columns exist
        if 'ingredients' not in recipes_df.columns or 'name_recipe' not in recipes_df.columns:
            raise KeyError("Required columns not found in the dataframe.")
        
        ingredient_list = []
        print("Enter ingredients one by one (type 'STOP' to finish):")
        
        # Collect ingredients from user input
        while True:
            try:
                ingredient = input("Enter ingredient: ").strip()
                if ingredient.lower() == 'stop':
                    break
                ingredient_list.append(ingredient)
            except Exception as e:
                print(f"Error in input: {e}")
        
        # Check if any ingredients were entered
        if not ingredient_list:
            print("No ingredients entered.")
            return
        
        matched_recipes = []
        for ingredient in ingredient_list:
            # Check for recipes containing the ingredient
            recipes = recipes_df[recipes_df['ingredients'].str.contains(ingredient, case=False, na=False)]
            if not recipes.empty:
                matched_recipes.extend(recipes['name_recipe'].tolist())
        
        # Output results
        if matched_recipes:
            print("Recipes containing the ingredients:")
            for recipe in set(matched_recipes):  # Use set to remove duplicates
                print(f"- {recipe}")
        else:
            print("No recipe found.")
    
    except AttributeError:
        print("Error: Input is not a valid pandas DataFrame.")
    except KeyError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
def suggest_missing_ingredients(recipes_df):
    """Suggest missing ingredients with exception handling"""
    try:
        recipe_name = input("Enter the name of the recipe: ").strip()
        if not isinstance(recipes_df, pd.DataFrame):
            raise TypeError("Invalid data format: recipes_df must be a pandas DataFrame")
            
        recipe = recipes_df[recipes_df['name_recipe'].str.contains(recipe_name, case=False, na=False)]
        if recipe.empty:
            raise RecipeNotFoundError(recipe_name)

        full_ingredients = recipe['ingredients'].iloc[0].split(',')
        full_ingredients = [ingredient.split('(')[0].strip() for ingredient in full_ingredients]

        print("Enter the ingredients you already have (type 'STOP' to finish):")
        partial_ingredients = []
        while True:
            ingredient = input("Enter ingredient: ").strip()
            if ingredient.lower() == 'stop':
                break
            partial_ingredients.append(ingredient)

        if not partial_ingredients:
            raise ValueError("No ingredients were provided")

        missing_ingredients = [item for item in full_ingredients if item not in partial_ingredients]
        if missing_ingredients:
            print("Missing Ingredients:")
            for ingredient in missing_ingredients:
                print(f"- {ingredient}")
        else:
            print("You have all the ingredients!")
            
    except RecipeNotFoundError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")
    except TypeError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
