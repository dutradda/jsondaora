build-virtualenv:
	@virtualenv venv --python python3.7 --prompt 'dataclassjson-> '

build-docs:
	@python -m mkdocs build
	@cp ./docs/changelog.md ./CHANGELOG.md
	@cd ./docs && \
	../scripts/replace-placeholders.py index.md ../README.md

deploy-docs: build-docs
	@python -m mkdocs gh-deploy

release-pypi:
	@flit publish
