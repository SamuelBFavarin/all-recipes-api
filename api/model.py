from typing import List
from pydantic import BaseModel

class Ingredient(BaseModel):
    name: str
    quantity: str

class Recipe(BaseModel):
    name: str
    description: str
    ingredients: List[Ingredient]

class RecipeRequest(BaseModel):
    recipe: Recipe
