.PHONY: help
.DEFAULT_GOAL := help
SHELL := /bin/bash

clean: clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python3 -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

test: ## run tests quickly with the default Python
	coverage run app/manage.py test && coverage report

install-dev-requirements: clean ## installs requirements locally
	pipenv install --dev

install-requirements: clean ## installs requirements locally
	pipenv install

create-venv: ## creates a virtual environment, if it doesn't exist
	test -d venv || python3 -m venv .venv

run-pre-commit: ## runs pre-commit hooks
	pre-commit run --all-files

lint: ## check style with flake8
	flake8 app/

black: ## run black
	black app/

createsuperuser: ## creates a superuser
	python app/manage.py createsuperuser

makemigrations: ## creates migrations
	python app/manage.py makemigrations

migrate: ## runs migrations
	python app/manage.py migrate

runserver: ## runs the server
	python app/manage.py runserver

shell_plus: ## runs the shell_plus
	python app/manage.py shell_plus
