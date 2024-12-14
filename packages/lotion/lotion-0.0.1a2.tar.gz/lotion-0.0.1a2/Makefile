.PHONY: test
test:
	@pipenv run pytest -m "not learning and not api"

.PHONY: test-current
test-current:
	@pipenv run pytest -m "current"


.PHONY: test-all
test-all:
	@pipenv run pytest -n auto --dist=loadfile

.PHONY: test-min
test-min:
	@pipenv run pytest -m "minimum"

.PHONY: release
release:
	python -m build
	twine upload --repository pypi dist/*
	rm -fr dist
