export PYTHONPATH = .

.PHONY: tests

help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

build-virtualenv:
	@virtualenv venv --python python3.7 --prompt 'dataclassjson-> '

build-docs:
	@python -m mkdocs build
	@cp ./docs/changelog.md ./CHANGELOG.md
	@cd ./docs && \
	../scripts/replace-placeholders.py index.md ../README.md

serve-docs:
	@mkdocs serve

deploy-docs: build-docs
	@python -m mkdocs gh-deploy

release-pypi:
	@flit publish

check-code:
	@isort --recursive --apply dataclassjson docs/src
	@black dataclassjson docs/src
	@flake8 dataclassjson docs/src
	@mypy --strict dataclassjson # docs/src/index

dependencies:
	@flit install --deps develop --extras all

tests:  ## Run tests
	@pytest -xvv --cov dataclassjson --no-cov-on-fail --cov-report=term-missing tests
