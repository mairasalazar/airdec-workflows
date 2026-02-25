.PHONY: migrate worker dev

migrate:
	alembic upgrade head

worker:
	uv run python -m app.workers

dev:
	uv run fastapi dev