COMPOSE_BASE := docker-compose
LOG_FILE := build.log

init-venv:
	python3 -m venv .venv

pytest:
	pytest -v fastapi;

build-up:
	$(COMPOSE_BASE)	-f docker-compose-local.yaml up -d --build --remove-orphans;

up:	
	$(COMPOSE_BASE)	-f docker-compose-local.yaml up -d;

restart:	
	$(COMPOSE_BASE)	-f docker-compose-local.yaml restart;

down:
	$(COMPOSE_BASE)	-f docker-compose-local.yaml down;