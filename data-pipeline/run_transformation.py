from typing import List
import pandas as pd
import datetime
import json


def read_json(file_path: str) -> dict:
    with open(file_path, 'r') as f:
        data = json.load(f)

    return data


def __remove_non_ingredient_words(ingredient_phrase:str) -> str:

    not_ingredient_word_list = ['tablespoons', 'tablespoon', 'teaspoons', 'teaspoon', 'stalks',
                                'cups', 'cup', 'spoon', 'ground', 'bottle', 'table', 'pinch',
                                'optional', 'ounce']

    for word in not_ingredient_word_list:
        ingredient_phrase = ingredient_phrase.replace(word, "")

    return ingredient_phrase


def __remove_special_chars(ingredient_phrase:str) -> str:
    return ''.join(filter(lambda x: x.isalpha() or x == '-' or x == " ", ingredient_phrase))


def __convert_ingredient_list_to_str(ingredients: List[str]) -> str:
    return f" {' | '.join(ingredients)} "

def clean_recipe_ingredients(recipes: List[dict]) -> List[dict]:

    for recipe in recipes:
        for row, ingredient in enumerate(recipe['ingredients']):
            recipe['ingredients'][row] = __remove_non_ingredient_words(recipe['ingredients'][row])
            recipe['ingredients'][row] = __remove_special_chars(recipe['ingredients'][row])

        recipe['ingredients'] = __convert_ingredient_list_to_str(recipe['ingredients'])

    return recipes


def transform_data(ingredients: List[dict], recipes: List[dict]) -> List[dict]:

    data_ingredient_recipe = []

    # For each ingredient, check if it appears in any of the recipe ingredients
    for ingredient in ingredients:
        ingredient_id = ingredient['ingredientId']
        ingredient_name = ingredient['term'].lower()

        for recipe in recipes:
            recipe_id = recipe['id']
            recipe_name = recipe['title']

            if f" {ingredient_name} " in recipe['ingredients']:
                data_ingredient_recipe.append({
                    'ingredient_id': ingredient['ingredientId'],
                    'recipe_id': recipe['id'],
                    'ingredient_name': ingredient['term'],
                    'recipe_name': recipe['title'],
                })

    return data_ingredient_recipe

def get_current_date_time(is_file_format:bool = False) -> str:
    if is_file_format:
        return datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":

    # load raw data
    print(f"Start load raw data process {get_current_date_time()}")
    ingredients = read_json('/app/datalake/raw/ingredients.json')
    recipes = read_json('/app/datalake/raw/recipes.json')

    # clean process
    print(f"Start clean raw data process {get_current_date_time()}")
    recipes_cleaned = clean_recipe_ingredients(recipes)

    # transform proccess
    final_data = transform_data(ingredients, recipes)

    # store final data as .json and .csv
    print(f"Start store data process {get_current_date_time()}")
    pd.DataFrame(final_data).to_csv(f"/app/datalake/clean/recipes_ingredients_{get_current_date_time(is_file_format=True)}.csv")

    print(f"Finished")
