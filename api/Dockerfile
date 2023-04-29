FROM python:3.10.9-slim

LABEL api all_recipes

WORKDIR /app
COPY ./api /app/
COPY ./data-pipeline/datalake /app/datalake/

# INSTALL REQUIRED LIBS
RUN pip install -r requirements.txt

# START SERVER
ENTRYPOINT uvicorn endpoint:app --host 0.0.0.0 --port 8000
