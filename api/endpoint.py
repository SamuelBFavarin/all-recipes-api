from fastapi import FastAPI
from core import ApiCore

app = FastAPI()

@app.get('/ingredient-cooccurrence')
def get_ingredient_cooccurrence(ingredient: str):

    core = ApiCore()
    ingredients = core.get_most_related_ingredients(ingredient)

    return {
        'ingredient': ingredient,
        'cooccurrence': ingredients
    }
