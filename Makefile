PIPELINE_NAME ?= recipes_pipeline
SERVER_NAME ?= recipes_api
TAG ?= dev

run-data-pipeline:    ./data-pipeline/Dockerfile

	"Data Pipeline Process started"
	docker build -t ${PIPELINE_NAME}:${TAG} -f ./data-pipeline/Dockerfile .
	docker run -t ${PIPELINE_NAME}:${TAG}

run-api-server:		./api/Dockerfile

	"Starting API server on http://127.0.0.1:8000/"
	docker build -t ${SERVER_NAME}:${TAG} -f ./api/Dockerfile .
	docker run -p 8000:8000 -t ${SERVER_NAME}:${TAG}
