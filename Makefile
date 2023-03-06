PYTHON_VERSION ?= 3.8

dist: clean-dist
	pip install --upgrade pip build
	python3 -m build .

setup: venv

venv: dev-packages.txt requirements.txt
	virtualenv venv --python=${PYTHON_VERSION}
	. venv/bin/activate && \
	pip3 install --upgrade pip && \
	pip3 install --requirement dev-packages.txt && \
	pip3 install --requirement requirements.txt

.PHONY: test
test: venv
	@ . venv/bin/activate && PYTHONPATH=src/ pytest -rsx tests/ src/ --cov ./src/requtests/ --no-cov-on-fail --cov-report term-missing --doctest-modules --doctest-continue-on-failure
	@ . venv/bin/activate && flake8  src --exclude '#*,~*,.#*'
	@ . venv/bin/activate && black --check src tests

.PHONY: clean
clean: clean-dist
	rm -rf venv

.PHONY: clean-dist
clean-dist:
	rm -rf build
	rm -rf src/requtests.egg-info
	rm -rf dist
