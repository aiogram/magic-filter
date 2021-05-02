.DEFAULT_GOAL := help

base_python := python3
py := poetry run
python := $(py) python

reports_dir := reports

package_dir := magic_filter
code_dir := $(package_dir) tests

help:
	@echo "magic-filter"


# =================================================================================================
# Environment
# =================================================================================================

clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -rf `find . -name .pytest_cache`
	rm -f `find . -type f -name '*.so' `
	rm -f `find . -type f -name '*.c' `
	rm -rf *.egg-info
	rm -f .coverage
	rm -f report.html
	rm -f .coverage.*
	rm -f .dmypy.json
	rm -rf {build,dist,site,.cache,.mypy_cache,reports,}


# =================================================================================================
# Code quality
# =================================================================================================

isort:
	$(py) isort $(code_dir)

black:
	$(py) black $(code_dir)

flake8:
	$(py) flake8 $(code_dir)

flake8-report:
	mkdir -p $(reports_dir)/flake8
	$(py) flake8 --format=html --htmldir=$(reports_dir)/flake8 $(code_dir)

mypy:
	$(py) mypy $(package_dir)

mypy-report:
	$(py) mypy $(package_dir) --html-report $(reports_dir)/typechecking

lint: isort black flake8 mypy

# =================================================================================================
# Tests
# =================================================================================================

test:
	$(py) pytest --cov=magic-filter --cov-config .coveragerc tests/

test-coverage:
	mkdir -p $(reports_dir)/tests/
	$(py) pytest --cov=magic-filter --cov-config .coveragerc --html=$(reports_dir)/tests/index.html tests/
	$(py) coverage html -d $(reports_dir)/coverage

test-coverage-report:
	python -c "import webbrowser; webbrowser.open('file://$(shell pwd)/reports/coverage/index.html')"

# =================================================================================================
# Project
# =================================================================================================

build: clean flake8-report mypy-report test-coverage docs docs-copy-reports
	mkdir -p site/simple
	poetry build
	mv dist site/simple/magic-filter
