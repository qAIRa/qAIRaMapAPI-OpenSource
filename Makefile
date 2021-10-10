.PHONY: build-test, test

DOCKER_COMPOSE_FILENAME := .docker/test/docker-compose.yml

build-test:
	docker-compose -f $(DOCKER_COMPOSE_FILENAME) build

test:
	docker-compose -f $(DOCKER_COMPOSE_FILENAME) up test
	docker-compose -f $(DOCKER_COMPOSE_FILENAME) down
