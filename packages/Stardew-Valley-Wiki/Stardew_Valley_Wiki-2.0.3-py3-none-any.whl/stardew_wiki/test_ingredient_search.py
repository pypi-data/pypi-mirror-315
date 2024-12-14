import unittest
from recipes.ingredient_search import list_all_ingredients, search_recipes_by_ingredients, suggest_missing_ingredients
import pandas as pd
from unittest.mock import patch

class TestIngredientSearch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize data at the class level (executed once)
        cls.recipes_df = pd.DataFrame({
            'name_recipe': ['Pizza', 'Omelet', 'Glazed Yams', 'Cheese Cauliflower'],
            'ingredients': [
                'Wheat Flour (1), Tomato (1), Cheese (1)',
                'Egg (1), Milk (1)',
                'Yam (1), Sugar (1)',
                'Cauliflower (1), Cheese (1)'
            ]
        })

    def setUp(self):
        print('Set up')

    def tearDown(self):
        print('Tear down')

    def test_list_all_ingredients(self):
        all_ingredients = list_all_ingredients(self.recipes_df)

        # Assertions for expected ingredients
        expected_ingredients = ['Wheat Flour', 'Tomato', 'Cheese', 'Egg', 'Milk', 'Yam', 'Sugar', 'Cauliflower']
        for ingredient in expected_ingredients:
            self.assertIn(ingredient, all_ingredients)

        # Assertions for unexpected ingredients
        self.assertNotIn('Garlic', all_ingredients)  
        self.assertNotIn('Pork', all_ingredients)  

        # Test empty DataFrame
        empty_df = pd.DataFrame(columns=['name_recipe', 'ingredients'])
        result = list_all_ingredients(empty_df)
        self.assertEqual(result, [])

        # Test DataFrame without ingredients column
        invalid_df = pd.DataFrame({'name': ['Recipe1', 'Recipe2']})
        with patch('builtins.print') as mocked_print:
            result = list_all_ingredients("not a dataframe")
            self.assertEqual(result, [])
            self.assertIn("Error:", str(mocked_print.call_args[0]))

    def test_search_recipes_by_ingredients(self):
        # Test searching with cheese
        with patch('builtins.input', side_effect=['Cheese', 'STOP']):
            with patch('builtins.print') as mocked_print:
                search_recipes_by_ingredients(self.recipes_df)
                output = "\n".join([args[0] for args, _ in mocked_print.call_args_list])
                self.assertIn("Pizza", output)
                self.assertIn("Cheese Cauliflower", output)
                self.assertNotIn("Omelet", output)
                self.assertNotIn("Glazed Yams", output)

        # Test searching with multiple ingredients
        with patch('builtins.input', side_effect=['Cheese', 'Milk', 'STOP']):
            with patch('builtins.print') as mocked_print:
                search_recipes_by_ingredients(self.recipes_df)
                output = "\n".join([args[0] for args, _ in mocked_print.call_args_list])
                self.assertIn("Omelet", output)
                self.assertIn("Cheese Cauliflower", output)

        # Test searching with non-existent ingredient
        with patch('builtins.input', side_effect=['Garlic', 'STOP']):
            with patch('builtins.print') as mocked_print:
                search_recipes_by_ingredients(self.recipes_df)
                output = "\n".join([args[0] for args, _ in mocked_print.call_args_list])
                self.assertIn("No recipe found.", output)

        # Test empty input
        with patch('builtins.input', side_effect=['STOP']):
            with patch('builtins.print') as mocked_print:
                search_recipes_by_ingredients(self.recipes_df)
                output = "\n".join([args[0] for args, _ in mocked_print.call_args_list])
                self.assertIn("No ingredients entered.", output)

        # Test DataFrame without required columns
        invalid_df = pd.DataFrame({'ingredients': ['Test1', 'Test2']})
        with patch('builtins.print') as mocked_print:
            search_recipes_by_ingredients(invalid_df)
            self.assertIn("Required columns not found", str(mocked_print.call_args[0]))

    def test_suggest_missing_ingredients(self):
        # Test normal case with missing ingredients
        with patch('builtins.input', side_effect=['Pizza', 'Tomato', 'STOP']):
            with patch('builtins.print') as mocked_print:
                suggest_missing_ingredients(self.recipes_df)
                output = "\n".join([args[0] for args, _ in mocked_print.call_args_list])
                self.assertIn("Wheat Flour", output)
                self.assertIn("Cheese", output)

        # Test case with all ingredients present
        with patch('builtins.input', side_effect=['Pizza', 'Tomato', 'Wheat Flour', 'Cheese', 'STOP']):
            with patch('builtins.print') as mocked_print:
                suggest_missing_ingredients(self.recipes_df)
                output = "\n".join([args[0] for args, _ in mocked_print.call_args_list])
                self.assertIn("You have all the ingredients!", output)

        # Test case-insensitive recipe matching
        with patch('builtins.input', side_effect=['pizza', 'Tomato', 'STOP']):
            with patch('builtins.print') as mocked_print:
                suggest_missing_ingredients(self.recipes_df)
                output = "\n".join([args[0] for args, _ in mocked_print.call_args_list])
                self.assertIn("Wheat Flour", output)
                self.assertIn("Cheese", output)

        # Test partial recipe name matching
        with patch('builtins.input', side_effect=['Pizz', 'Tomato', 'STOP']):
            with patch('builtins.print') as mocked_print:
                suggest_missing_ingredients(self.recipes_df)
                output = "\n".join([args[0] for args, _ in mocked_print.call_args_list])
                self.assertIn("Wheat Flour", output)
                self.assertIn("Cheese", output)

        # Test recipe not found
        with patch('builtins.input', side_effect=['Garlic Bread', 'STOP']):
            with patch('builtins.print') as mocked_print:
                suggest_missing_ingredients(self.recipes_df)
                output = "\n".join([args[0] for args, _ in mocked_print.call_args_list])
                self.assertIn("Recipe 'Garlic Bread' not found", output)

        # Test no ingredients provided
        with patch('builtins.input', side_effect=['Pizza', 'STOP']):
            with patch('builtins.print') as mocked_print:
                suggest_missing_ingredients(self.recipes_df)
                output = "\n".join([args[0] for args, _ in mocked_print.call_args_list])
                self.assertIn("No ingredients were provided", output)

        # Test invalid DataFrame
        with patch('builtins.input', side_effect=['Pizza']):
            with patch('builtins.print') as mocked_print:
                suggest_missing_ingredients(None)
                output = "\n".join([args[0] for args, _ in mocked_print.call_args_list])
                self.assertIn("Invalid data format", output)

    @classmethod
    def tearDownClass(cls):
        # Clean up class-level resources
        cls.recipes_df = None

if __name__ == '__main__':
    unittest.main()


# class TestIngredientSearch(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         # Initialize data at the class level (executed once)
#         cls.recipes_df = pd.DataFrame({
#             'name_recipe': ['Pizza', 'Omelet', 'Glazed Yams', 'Cheese Cauliflower'],
#             'ingredients': [
#                 'Wheat Flour (1), Tomato (1), Cheese (1)',
#                 'Egg (1), Milk (1)',
#                 'Yam (1), Sugar (1)',
#                 'Cauliflower (1), Cheese (1)'
#             ]
#         })

#     def setUp(self):
#         print('Set up')

#     def tearDown(self):
#         print('Tear down')

#     def test_list_all_ingredients(self):
#         all_ingredients = list_all_ingredients(self.recipes_df)

#         # Assertions for expected ingredients
#         self.assertIn('Tomato', all_ingredients)
#         self.assertIn('Cheese', all_ingredients)

#         # Assertions for unexpected ingredients
#         self.assertNotIn('Garlic', all_ingredients)  
#         self.assertNotIn('Pork', all_ingredients)  

#     def test_search_recipes_by_ingredients(self):
#         with patch('builtins.input', side_effect=['Cheese', 'STOP']):
#             with patch('builtins.print') as mocked_print:
#                 search_recipes_by_ingredients(self.recipes_df)
#                 output = "\n".join([args[0] for args, _ in mocked_print.call_args_list])
#                 self.assertIn("Pizza", output)
#                 self.assertIn("Cheese Cauliflower", output)
#                 self.assertNotIn("Omelet", output)
#                 self.assertNotIn("Glazed Yams", output)

#         with patch('builtins.input', side_effect=['Garlic', 'STOP']):
#             with patch('builtins.print') as mocked_print:
#                 search_recipes_by_ingredients(self.recipes_df)
#                 output = "\n".join([args[0] for args, _ in mocked_print.call_args_list])
#                 self.assertIn("No recipe found.", output)

#     def test_suggest_missing_ingredients(self):
#         # Test case 1: Normal case - some missing ingredients
#         with patch('builtins.input', side_effect=['Pizza', 'Tomato', 'Wheat Flour', 'STOP']):
#             with patch('builtins.print') as mocked_print:
#                 suggest_missing_ingredients(self.recipes_df)
#                 output = "\n".join([args[0] for args, _ in mocked_print.call_args_list])
#                 self.assertIn("Cheese", output)
#                 self.assertNotIn("Yam", output)
#                 self.assertNotIn("Tomato", output)
#                 self.assertNotIn("Milk", output)
        
#         # Test case 2: All ingredients present
#         with patch('builtins.input', side_effect=['Pizza', 'Tomato', 'Wheat Flour', "Cheese", 'STOP']):
#             with patch('builtins.print') as mocked_print:
#                 suggest_missing_ingredients(self.recipes_df)
#                 output = "\n".join([args[0] for args, _ in mocked_print.call_args_list])
#                 self.assertIn("You have all the ingredients!", output)

#         # Test case 3: Recipe not found (Garlic)
#         with patch('builtins.input', side_effect=['Garlic', 'STOP']):
#             with patch('builtins.print') as mocked_print:
#                 suggest_missing_ingredients(self.recipes_df)
#                 output = "\n".join([args[0] for args, _ in mocked_print.call_args_list])
#                 self.assertIn("Error: Recipe 'Garlic' not found in the database", output)

#         # Test case 4: Invalid DataFrame
#         with patch('builtins.input', side_effect=['Pizza']):
#             with patch('builtins.print') as mocked_print:
#                 suggest_missing_ingredients(None)  # Pass None instead of DataFrame
#                 output = "\n".join([args[0] for args, _ in mocked_print.call_args_list])
#                 self.assertIn("Error: Invalid data format", output)
        
#         # Test case 5: No ingredients were provided
#         with patch('builtins.input', side_effect=['Pizza', 'STOP']):
#             with patch('builtins.print') as mocked_print:
#                 suggest_missing_ingredients(self.recipes_df)
#                 output = "\n".join([args[0] for args, _ in mocked_print.call_args_list])
#                 self.assertIn("Error: No ingredients were provided", output)

#     @classmethod
#     def tearDownClass(cls):
#         # Clean up class-level resources
#         cls.recipes_df = None
