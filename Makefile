.PHONY: start build rebuild stop run-app docker-run bash clean-docker clean help

PROJECT_NAME=novalex-api
PROJECT_CONTAINER_NAME=api
DOCKER_COMPOSE=docker/docker-compose.yaml

start: ## Start services
	@printf "\n=> Start services...\n\n"
	@docker compose -f $(DOCKER_COMPOSE) -p $(PROJECT_NAME) up

build: ## Build services
	@printf "\n=> Build services...\n\n"
	@docker compose -f $(DOCKER_COMPOSE) -p $(PROJECT_NAME) build --force-rmmake

rebuild: ## Rebuild and start services
	@printf "\n=> Rebuild services...\n\n"
	# remove containers
	@docker compose -f $(DOCKER_COMPOSE) -p $(PROJECT_NAME) down --remove-orphans
	@docker compose -f $(DOCKER_COMPOSE) -p $(PROJECT_NAME) build --no-cache --force-rm
	@docker compose -f $(DOCKER_COMPOSE) -p $(PROJECT_NAME) up -d

stop: ## Stop services
	@printf "\n=> Stop services...\n\n"
	@docker compose -f $(DOCKER_COMPOSE) -p $(PROJECT_NAME) down --remove-orphans

run-app: ## Run api service
	@printf "\n=> Run api service...\n\n"
	@docker compose -f $(DOCKER_COMPOSE) -p $(PROJECT_NAME) up -d $(PROJECT_CONTAINER_NAME)

docker-run: ## Starts FastAPI service in docker container
	@docker run -p 8000:8000 -it $(PROJECT_NAME) gunicorn src.main:create_fastapi_app --worker-class uvicorn.workers.UvicornWorker --reload --workers 1 -b 0.0.0.0:8000

bash:
	@docker compose -f $(DOCKER_COMPOSE) -p $(PROJECT_NAME) exec $(PROJECT_CONTAINER_NAME) sh

clean-docker: ## Removing all: containers, images and volumes
	@printf "\n=> Removing containers and images...\n\n"
	@docker compose -f $(DOCKER_COMPOSE) down --remove-orphans
	@docker compose -f $(DOCKER_COMPOSE) rm --stop --force -v $(PROJECT_CONTAINER_NAME)
	@docker rmi $(PROJECT_NAME) || printf=""
	@docker image prune -af
	@docker system prune --volumes

clean: ## Clean all useless data
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -f `find . -type f -name '@*' `
	rm -f `find . -type f -name '#*#' `
	rm -f `find . -type f -name '*.orig' `
	rm -f `find . -type f -name '*.rej' `
	rm -f .coverage
	rm -rf htmlcov
	rm -rf docs/_build/
	rm -rf coverage.xml
	rm -rf dist

help:
	@egrep -h '\s##\s' $(MAKEFILE_LIST) \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-30s\033[0m %s\n", $$1, $$2}'
