FROM python:3.10.9-slim

LABEL data_pipeline all_recipes

WORKDIR /app
COPY ./data-pipeline /app/

# INSTALL REQUIRED LIBS
RUN pip install -r requirements.txt
ENTRYPOINT python run_transformation.py
