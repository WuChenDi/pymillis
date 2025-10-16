.PHONY: maint clean test build install-dev

install-dev:
	pip install -e .
	pip install -r requirements/dev.txt

maint:
	pip-compile -U requirements/dev.in

clean:
	python -m pip install pyclean
	pyclean .
	rm -rf tests/__pycache__ pymillis/__pycache__ htmlcov docs/_build dist pymillis.egg-info .pytest_cache .mypy_cache .benchmarks

test:
	pytest tests --cov=pymillis --cov-report term-missing -vv --cov-report html --durations=3

build:
	python -m build
