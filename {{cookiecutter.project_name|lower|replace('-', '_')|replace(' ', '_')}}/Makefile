black:
	poetry run black src --check

black!:
	poetry run black src

isort:
	poetry run isort src/* --check --settings-path ./pyproject.toml --diff

isort!:
	poetry run isort src/* --settings-path ./pyproject.toml

build:
	pip install -U pip setuptools\<60.0.0
	poetry install --no-dev

build-dev:
	pip install -U pip setuptools\<60.0.0
	poetry install

build-requirements:
	poetry export --without-hashes --with-credentials > requirements.txt

docker-compose:
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose -f docker/docker-compose.yml -p project up

docker-compose-d:
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose -f docker/docker-compose.yml -p project up -d

docker-compose-db:
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose -f docker/docker-compose.yml -p project run -p 5432:5432 db

docker-compose-build:
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose -f docker/docker-compose.yml -p project build

docker-compose-migrations:
	docker-compose -f docker/docker-compose.yml -p project exec web alembic revision --autogenerate -m $(name)

docker-compose-migrate:
	docker-compose -f docker/docker-compose.yml -p project exec -T web alembic upgrade head

docker-compose-down:
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose -f docker/docker-compose.yml -p project down

docker-compose-test:
	docker-compose -f docker/docker-compose.yml -p project exec -T web pytest

docker-compose-down-v:
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose -f docker/docker-compose.yml -p project down -v

docker-compose-bash:
	docker-compose -f docker/docker-compose.yml -p project exec web bash

docker-compose-db-bash:
	docker-compose -f docker/docker-compose.yml -p project exec db bash
