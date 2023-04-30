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
        result_df = result_df.sort_values('total', ascending=False).head(10)
        return result_df.to_dict(orient='records')

    def get_most_similar_recipes(self, recipe: Recipe) -> dict:

        ingredients = [ingredient.name.lower() for ingredient in recipe.ingredients]
        df = self.df_clean_recipes_ingredients

        # create all_recipes sub-query
        all_recipes = df.groupby('recipe_id').size().reset_index(name='total_ingredients')

        # create match_recipes sub-query
        match_recipes = df.loc[df['ingredient_name'].isin(ingredients)]
        match_recipes = match_recipes.groupby(['recipe_id', 'recipe_name']).size().reset_index(name='total_similar_ingredient')
        match_recipes = match_recipes.sort_values(by='total_similar_ingredient', ascending=False)

        # join the sub-queries and calculate recipe similarity
        result = all_recipes.merge(match_recipes, on='recipe_id')
        result['recipe_similarity'] = (result['total_similar_ingredient'] / result['total_ingredients']) * 0.4 \
                                    + (result['total_similar_ingredient'] / len(ingredients)) * 0.6

        # select and order the final result
        result = result[['recipe_id', 'recipe_name', 'recipe_similarity']]
        result = result.sort_values(by='recipe_similarity', ascending=False)

        # limit to top 5
        result = result.head(5)
        return result.to_dict(orient='records')
