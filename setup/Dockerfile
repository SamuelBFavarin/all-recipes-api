FROM python:3.10.9-slim

LABEL datalake_setup all_recipes

WORKDIR /app
COPY ./setup /app/
COPY ./data-pipeline /app/

# INSTALL GSUTIL LIB
RUN pip install gsutil

# ADD PERMISSIONS TO SETUP.SH
RUN chmod 777 ./setup.sh

ENTRYPOINT ["./setup.sh"]
