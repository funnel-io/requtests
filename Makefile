PYTHON_VERSION ?= 3.9

dist: clean-dist venv
	. venv/bin/activate && python3 -m build .

setup: venv

venv: dev-requirements.txt requirements.txt
	virtualenv venv --python=${PYTHON_VERSION}
	. venv/bin/activate && \
	pip3 install --upgrade pip && \
	pip3 install \
	--requirement dev-requirements.txt \
	--requirement requirements.txt

.PHONY: test
test: venv
	@ . venv/bin/activate && PYTHONPATH=src/ pytest -vv -rsx tests src --cov ./src/requtests --no-cov-on-fail --cov-report term-missing --doctest-modules --doctest-continue-on-failure
	@ . venv/bin/activate && flake8 src --exclude '#*,~*,.#*'
	@ . venv/bin/activate && black --check src tests

.PHONY: test-focus
test-focus: venv/setup.txt
	@ . venv/bin/activate && PYTHONPATH=src/ pytest -vv -m focus -rsx tests src --cov ./src/requtests --no-cov-on-fail --cov-report term-missing --doctest-modules --doctest-continue-on-failure
	@ . venv/bin/activate && flake8 src --exclude '#*,~*,.#*'
	@ . venv/bin/activate && black --check src tests

.PHONY: clean
clean: clean-dist
	rm -rf venv

.PHONY: clean-dist
clean-dist:
	rm -rf build
	rm -rf src/requtests.egg-info
	rm -rf dist
