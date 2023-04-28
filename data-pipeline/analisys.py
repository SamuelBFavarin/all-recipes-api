# query = """"
# -- MOST COMOM RELATED INGREEDIENT
# SELECT
#   recipes.ingredient_name,
#   COUNT(1) AS total,
#   ARRAY_AGG(recipes.recipe_id) AS recipe_ids
# FROM `dev-pineapple-pipeline.dev_recipes.recipes` AS ingredient_selected
# INNER JOIN `dev-pineapple-pipeline.dev_recipes.recipes` AS recipes
#   ON recipes.recipe_id = ingredient_selected.recipe_id
# WHERE
#   ingredient_selected.ingredient_name = 'salt' AND
#   recipes.ingredient_name != 'salt'
# GROUP BY 1
# ORDER BY 2 DESC;


# -- CALC SIMILAR RECIPES BY TOTAL INGREDIENTS SHAREDS
# SELECT
#   recipe_id,
#   recipe_name,
#   ARRAY_AGG(ingredient_name) AS ingredients,
#   ARRAY_LENGTH(ARRAY_AGG(ingredient_name)) AS total_similar_ingredients
# FROM `dev-pineapple-pipeline.dev_recipes.recipes` AS recipe
# WHERE recipe.ingredient_name IN ('raisins', 'bananas', 'raspberries', 'blueberries', 'dried cranberries', 'golden raisins', 'blackberries')
# GROUP BY 1, 2
# ORDER BY 4 DESC
# LIMIT 5;
# """"
