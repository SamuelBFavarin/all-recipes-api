PIPELINE_NAME ?= recipes_pipeline
SERVER_NAME ?= recipes_api
DATALAKE_NAME ?= recipes_datalake
TAG ?= dev

run-datalake-setup:		./setup/Dockerfile

	echo "Datalake setup"
	docker build -t ${DATALAKE_NAME}:${TAG} -f ./setup/Dockerfile .
	docker run -v $(PWD)/data-pipeline/datalake:/app/datalake -t ${DATALAKE_NAME}:${TAG}

run-data-pipeline:    ./data-pipeline/Dockerfile

	echo "Data Pipeline Process started"
	docker build -t ${PIPELINE_NAME}:${TAG} -f ./data-pipeline/Dockerfile .
	docker run -v $(PWD)/data-pipeline/datalake:/app/datalake -t ${PIPELINE_NAME}:${TAG}

run-api-server:		./api/Dockerfile

	echo "Starting API server on http://127.0.0.1:8000/"
	docker build -t ${SERVER_NAME}:${TAG} -f ./api/Dockerfile .
	docker run -p 8000:8000 -t ${SERVER_NAME}:${TAG}
