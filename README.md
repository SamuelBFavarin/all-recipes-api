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
