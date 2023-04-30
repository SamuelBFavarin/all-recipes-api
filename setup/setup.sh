#!/bin/bash

echo "Download recipe.json raw data"
mkdir /app/datalake/raw/
gsutil cp gs://all-recipes-data/datalake/raw/recipes.json /app/datalake/raw

echo "Download ingredients.json raw data"
gsutil cp gs://all-recipes-data/datalake/raw/ingredients.json /app/datalake/raw

ls /app/datalake/raw

echo "Download recipes_ingredients.json clean data"
mkdir /app/datalake/clean/
gsutil cp gs://all-recipes-data/datalake/clean/recipes_ingredients_2023_04_30_03_33_39.csv /app/datalake/clean

ls /app/datalake/clean
