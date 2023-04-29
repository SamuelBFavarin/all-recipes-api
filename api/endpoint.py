from fastapi import FastAPI, HTTPException
from core import ApiCore

app = FastAPI()

@app.get('/ingredient-cooccurrence')
def get_ingredient_cooccurrence(ingredient: str):

    core = ApiCore()

    if core.is_valid_ingredient(ingredient):
        cooccurrence_ingredients = core.get_most_related_ingredients(ingredient)
        return {'ingredient': ingredient, 'cooccurrence': cooccurrence_ingredients}
    else:
        raise HTTPException(status_code=404, detail="Invalid ingredient")
