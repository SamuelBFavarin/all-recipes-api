import pandas as pd
from typing import List


class ApiCore:

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self):
        self.df = self.__load_data("/app/datalake/clean/recipes_ingredients_2.csv")

    def __repr__(self) -> str:
        return f"{type(self).__name__}(recipes_ingredients={self.df})"

    def __load_data(self, data_path:str) -> pd.DataFrame:
        return pd.read_csv(data_path)

    def get_most_related_ingredients(self, ingredient: str) -> dict:

        ingredient_df = self.df[self.df['ingredient_name'] == ingredient]
        merged_df = pd.merge(ingredient_df, self.df[self.df['ingredient_name'] != ingredient], on='recipe_id', suffixes=('_selected', ''))
        result_df = merged_df.groupby('ingredient_name').size().reset_index(name='total')
        result_df = result_df.sort_values('total', ascending=False).head(10)
        return result_df.to_dict(orient='records')

    def get_most_similar_recipes(self, ingredients: List[str]) -> pd.DataFrame:

        filtered_df = self.df[self.df['ingredient_name'].isin(ingredients)]
        result_df = filtered_df.groupby(['recipe_id', 'recipe_name']).agg({'ingredient_name': lambda x: list(x), 'recipe_id': 'count'}).rename(columns={'ingredient_name': 'ingredients', 'recipe_id': 'total_similar_ingredients'})
        result_df = result_df.sort_values('total_similar_ingredients', ascending=False).head(10)
        return result_df


if __name__ == "__main__":

    core = ApiCore()

    df_res = core.get_most_related_ingredients('salt')
    print(df_res)

    df_res = core.get_most_similar_recipes(['milk', 'butter', 'egg', 'cocoa'])
    print(df_res)
