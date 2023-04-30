from fastapi import FastAPI, HTTPException
from core import ApiCore
from model import RecipeRequest

app = FastAPI()

@app.get('/ingredient-cooccurrence')
def get_ingredient_cooccurrence(ingredient: str):

    core = ApiCore()

    if core.is_valid_ingredient(ingredient):
        cooccurrence_ingredients = core.get_most_related_ingredients(ingredient)
        return {'ingredient': ingredient, 'cooccurrence': cooccurrence_ingredients}
    else:
        raise HTTPException(status_code=404, detail="Invalid ingredient")

@app.post('/recipe-duplicates')
def post_recipe_duplicates(recipe_request: RecipeRequest):

    core = ApiCore()
    similar_recipes = core.get_most_similar_recipes(recipe_request.recipe)
    return {'duplicates': similar_recipes}
