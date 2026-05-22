.PHONY: lint format run

lint:
	ruff check .

format:
	ruff format .
	ruff check . --fix

run:
	uvicorn app.main:app --reload
