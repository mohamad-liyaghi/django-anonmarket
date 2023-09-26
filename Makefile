.PHONY: help build run stop

help:
	@echo "Available targets:"
	@echo "  help    - Show this help message."
	@echo "  build   - Build the docker image."
	@echo "  run     - Run the docker container."
	@echo "  stop    - Stop the docker container."
	@echo "  migrations - Create migrations."
	@echo "  migrate - Migrate"


build:
	docker compose build

run:
ifeq ($(DETACHED),true)
	docker compose up -d
else
	docker compose up
endif

stop:
	docker compose down

migrations:
	docker exec tsuna-streaming-backend python manage.py makemigrations

migrate:
	docker exec tsuna-streaming-backend python manage.py migrate