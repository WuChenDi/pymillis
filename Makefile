maint:
	pip-compile -U requirements/dev.in

clean:
	python -m pip install pyclean
	pyclean .
	rm -rf tests/__pycache__ pyms/__pycache__ htmlcov docs/_build dist pyms.egg-info .pytest_cache .mypy_cache .benchmarks

test:
	pytest tests --cov --cov-report term-missing -vv --cov-report html --durations=3 --timeout=60 pypdf

testtype:
	pytest tests --cov --cov-report term-missing -vv --cov-report html --durations=3 --timeout=30 --typeguard-packages=pypdf

build: clean
	python -m build
