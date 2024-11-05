.PHONY: install install-dev run test build service_run service_stop service_clear

# Install dependencies from requirements.txt
install:
	pip install -r requirements.txt

# Install development dependencies
install-dev:
	pip install -r requirements-dev.txt

# Run the service using Docker Compose
service_run:
	docker-compose up --build -d

# Stop the service
service_stop:
	docker-compose stop

# Remove the service and its containers
service_clear:
	docker-compose down --remove-orphans --volumes

# Run the application locally with Uvicorn and load environment variables from .env
run:
	cd src; uvicorn api:app --host 0.0.0.0 --port 8003 --env-file .env

# Run tests with pytest, currently not realised
test:
	pytest
