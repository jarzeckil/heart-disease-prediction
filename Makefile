.PHONY: install format lint test

help:
	@grep -E '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-30s\033[0m %s\n", $$1, $$2}'

install: ## install dependencies
	poetry install

format: ## auto format files
	ruff format .
	ruff check . --fix

lint: ## check formating
	ruff check .
	ruff format --check

test: ## run tests
	poetry run pytest tests/
