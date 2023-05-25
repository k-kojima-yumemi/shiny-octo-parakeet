.PHONY: format
format: black isort flake8 mypy

.PHONY: black
black:
	black .

.PHONY: black-ci
black-ci:
	black --check .

.PHONY: isort
isort:
	isort .

.PHONY: isort-ci
isort-ci:
	isort --check-only .

.PHONY: flake8
flake8:
	pflake8 .

.PHONY: mypy
mypy:
	mypy .
