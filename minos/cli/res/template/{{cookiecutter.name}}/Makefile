install:
	poetry install

reformat: ## check code coverage quickly with the default Python
	poetry run black --line-length 120 src tests
	poetry run isort src tests

lint: ## check style with flake8
	poetry run flake8

test: ## run tests quickly with the default Python
	poetry run pytest

coverage: ## check code coverage quickly with the default Python
	poetry run coverage run -m pytest
	poetry run coverage report -m
	poetry run coverage xml
