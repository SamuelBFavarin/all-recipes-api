from typing import List
import pandas as pd
import json


def read_json(file_path: str) -> dict:
    with open(file_path, 'r') as f:
        data = json.load(f)

    return data


def write_json(file_path: str, data: List[dict]) -> None:
    with open(file_path, 'w') as f:
        json.dump(data, f)


def clean_recipe_ingredients(recipes: List[dict]) -> List[dict]:

    # Create a set of unique ingredient terms for each recipe
    not_ingredient_words = ['tablespoons', 'tablespoon', 'teaspoons', 'teaspoon', 'stalks',
                            'cups', 'cup', 'spoon', 'ground', 'bottle', 'table', 'pinch',
                            'mi', 'su', 'min']

    for recipe in recipes:
        for row, ingredient in enumerate(recipe['ingredients']):
            for not_ingredient_word in not_ingredient_words:
                recipe['ingredients'][row] = recipe['ingredients'][row].replace(not_ingredient_word, " ")

    return recipes


def transform_data(ingredients: List[dict], recipes: List[dict]) -> List[dict]:

    data_ingredient_recipe = []
    unique_pairs = set()

    # transform a list[str] to str
    recipe_ingredients = [', '.join(
        [ingredient.lower() for ingredient in recipe['ingredients']]
    ) for recipe in recipes]


    # For each ingredient, check if it appears in any of the recipe ingredients
    for ingredient in ingredients:
        ingredient_id = ingredient['ingredientId']
        ingredient_name = ingredient['term'].lower()

        for row, recipe in enumerate(recipes):
            recipe_id = recipe['id']
            recipe_name = recipe['title']

            if ingredient_name in recipe_ingredients[row] \
                and len(ingredient_name) > 2 and (ingredient_id, recipe_id) not in unique_pairs:

                data_ingredient_recipe.append({
                    'ingredient_id': ingredient['ingredientId'],
                    'recipe_id': recipe['id'],
                    'ingredient_name': ingredient['term'],
                    'recipe_name': recipe['title'],
                })

                unique_pairs.add((ingredient_id, recipe_id))

                print(data_ingredient_recipe[-1])

    return data_ingredient_recipe


if __name__ == "__main__":

    # load json
    ingredients = read_json('/Users/samuel/Documents/GitHub/all-recipes-api/data-pipeline/data/raw/ingredients.json')
    recipes = read_json('/Users/samuel/Documents/GitHub/all-recipes-api/data-pipeline/data/raw/recipes.json')

    # clean proccess
    recipes_cleaned = clean_recipe_ingredients(recipes)

    # transform proccess
    final_data = transform_data(ingredients, recipes)

    # store final data as .json and .csv
    write_json('/Users/samuel/Documents/GitHub/all-recipes-api/data-pipeline/data/clean/recipes_ingredients_2.json', final_data)
    df = pd.read_json('/Users/samuel/Documents/GitHub/all-recipes-api/data-pipeline/data/clean/recipes_ingredients_2.json')
    df.to_csv('/Users/samuel/Documents/GitHub/all-recipes-api/data-pipeline/data/clean/recipes_ingredients_2.csv')

    # Display the DataFrame
    print(df)
