export PYTHONPATH = .

.PHONY: tests

help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

build-virtualenv:
	@virtualenv venv --python python3.7 --prompt 'jsondaora-> '

build-docs:
	@mkdocs build
	@cp ./docs/changelog.md ./CHANGELOG.md
	@cd ./docs && \
	../scripts/replace-placeholders.py index.md ../README.md

serve-docs:
	@mkdocs serve

deploy-docs: build-docs
	@mkdocs gh-deploy

deploy: deploy-docs
	@make release-pypi

release-pypi:
	@flit publish

check-code: isort black flake8 mypy

isort:
	@isort --recursive --apply jsondaora docs/src

black:
	@black jsondaora docs/src

flake8:
	@flake8 jsondaora docs/src

mypy:
	@mypy --strict jsondaora # docs/src/index

dependencies:
	@flit install --deps develop --extras all

tests:  ## Run tests
	@pytest -xvv --cov jsondaora --no-cov-on-fail --cov-report=term-missing jsondaora/tests
	@docs/src/test.sh

integration:
	@make check-code
	@make tests
