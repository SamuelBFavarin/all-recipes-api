from typing import List
from model import Recipe
import pandas as pd
import logging
import os


class ApiCore:

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self):
        self.df_clean_recipes_ingredients = self.__load_data(self.__get_path_last_clean_table())
        self.df_raw_ingredients = self.__load_data("/app/datalake/raw/ingredients.json")

    def __repr__(self) -> str:
        return f"{type(self).__name__}(recipes_ingredients={self.df_clean_recipes_ingredients})"

    def __get_path_last_clean_table(self) -> str:
        return f"/app/datalake/clean/{os.listdir('/app/datalake/clean')[0]}"

    def __load_data(self, data_path:str) -> pd.DataFrame | None:

        file_extension = data_path.split('.')[-1]

        if file_extension == 'csv':
            return pd.read_csv(data_path)
        elif file_extension == 'json':
            return pd.read_json(data_path)
        else:
            logging.error("Invalid extension")

    def is_valid_ingredient(self, ingredient:str) -> bool:
        return True if len(self.df_raw_ingredients[self.df_raw_ingredients['searchValue'] == ingredient.lower()]) > 0 else False

    def get_most_related_ingredients(self, ingredient: str) -> dict:

        ingredient = ingredient.lower()
        ingredient_df = self.df_clean_recipes_ingredients[self.df_clean_recipes_ingredients['ingredient_name'] == ingredient]
        others_ingredients =  self.df_clean_recipes_ingredients[self.df_clean_recipes_ingredients['ingredient_name'] != ingredient]

        merged_df = pd.merge(ingredient_df, others_ingredients, on='recipe_id', suffixes=('_selected', ''))
        result_df = merged_df.groupby('ingredient_name').size().reset_index(name='total')
        result_df = result_df.sort_values('total', ascending=False).head(5)
        return result_df.to_dict(orient='records')

    def get_most_similar_recipes(self, recipe: Recipe) -> dict:

        ingredients = [ingredient.name.lower() for ingredient in recipe.ingredients]

        filtered_df = self.df_clean_recipes_ingredients[self.df_clean_recipes_ingredients['ingredient_name'].isin(ingredients)]
        grouped_df = filtered_df.groupby(['recipe_id', 'recipe_name']).agg(total_similar_ingredients=('ingredient_name', 'count'))
        result_df = grouped_df.sort_values(by='total_similar_ingredients', ascending=False).head(5)

        return result_df.to_dict(orient='list')
