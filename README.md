# The all recipes API 🍝
This repository contains a data pipeline process and an API designed to provide recipe information. The data pipeline processes, performs data cleaning and transformation, and stores the data in a datalake. The API provides endpoints for users to retrieve and filter similar recipes and common ingredients based on parameters. 

## File Structure

    all-recipes-api/
    ├── api/
    │   ├── core.py
    │   ├── endpoint.py
    │   ├── model.py
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   ├── __init__.py
    ├── data-pipeline/
    │   ├── datalake/
    │   │   ├── raw/ 
    |   │   │   ├── ingredients.json
    |   │   │   ├── recipes.json    
    │   │   ├── clean/        
    |   │   │   ├── recipes_ingredients_Y_M_D_H_m_S.csv   
    │   ├── run_transformation.py
    │   ├── Dockerfile
    │   ├── requirements.txt
    ├── doc/
    │   ├── all-recipes-api.jpg
    │   ├── logic_sql_base.txt
    ├── setup/
    │   ├── Dockerfile
    │   ├── setup.sh
    ├── .gitignore
    ├── Makefile
    └── README.md

This project is structured into several folders to organize the different parts of the data pipeline and API: 
- The `api` folder contains files responsible for creating and providing endpoints for users using the FastAPI framework;
- The `data-pipeline` folder contains the data lake structure and scripts responsible for cleaning and transforming the data. Raw data is stored as `.json` and clean data is stored as `.csv`, organized by date/time. Pandas is used as the framework for manipulating the data;
- The `doc` folder provides assets for documenting the project;
- The `setup` folder provides an easy way to set up the data lake structure. Running this process downloads all required files from GCP Storage buckets to your machine automatically. 
- The `Makefile` provides an easy way to run all parts of the repo. For more datails, please, check the "How to run" documentation.

## Project Architecture

This diagram illustrates the architecture of this project. The project is divided into two main parts: the data pipeline and the API.

![enter image description here](https://raw.githubusercontent.com/SamuelBFavarin/all-recipes-api/main/doc/all-recipes-diagram.jpg)

The data pipeline is responsible for pre-processing and transforming raw data into a clean and organized format that can be easily queried by the API. Raw data is ingested into the pipeline from an external source (in this case, Google Cloud Storage) and is cleaned and transformed using a combination of Python and Pandas. The cleaned and transformed data is then stored in a structured format (CSV files organized by date/time).

The clean file follows a structured approach by establishing a relationship between recipes and ingredients. Each row in the file represents a relationship between a recipe and an ingredient. It is important to note that an ingredient can be present in more than one recipe, and a recipe can have multiple ingredients.

 ```
  id,ingredient_id,recipe_id,ingredient_name,recipe_name
  0,e01cac82-90ba-4267-8201-4d4d16332fb4,11125,salt,Baker's Clay
  1,e01cac82-90ba-4267-8201-4d4d16332fb4,11126,salt,Dough Ornament Recipe
  2,e01cac82-90ba-4267-8201-4d4d16332fb4,12480,salt,Cajun Sweet Dough
  3,e01cac82-90ba-4267-8201-4d4d16332fb4,145853,salt,Unbelievable Fish Batter
  4,e01cac82-90ba-4267-8201-4d4d16332fb4,152881,salt,Simple Cajun Seasoning
  5,e01cac82-90ba-4267-8201-4d4d16332fb4,165384,salt,Bananas Foster Belgian Waffles
 ```


The API is responsible for providing access to the processed data to end-users. The API is built using the FastAPI framework and consists of 2 endpoints that can be queried to retrieve data. 

The first endpoint `/ingredient-cooccurrence` identify ingredients that are commonly used together with a specified ingredient, such as 'banana'. The output provides a top 10 most frequently occurring ingredients used with the specified ingredient.

The second endpoint `/recipe-duplicates` returns a list of the top 5 recipes that are most similar to the recipe presented by the user. The similarity between recipes is determined using the common ingredients between them. The similarity metric is calculated using the following equation:

$similarity = \frac{TotalSimilarIngredient}{TotalIngredientsRecipeFound} \times 0.4 + \frac{TotalSimilarIngredient}{TotalIngredientsNewRecipe} \times 0.6$
