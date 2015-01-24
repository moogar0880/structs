.PHONY: docs

dev:
    # Install recommended dev packages
	pip install -U pip setuptools nose wheel

test:
	# This runs all of the tests. To run an individual test, run nosetests with
	# a module path specified
	nosetests tests

coverage:
    # Run the test suite with coverage enabled
	nosetests --verbose --with-coverage structures tests

publish:
    # Register and upload packages to PyPi
	python setup.py register
	python setup.py sdist upload
	python setup.py bdist_wheel upload

docs-init:
    # Install packages required to build documentation
	pip install Sphinx

docs:
    # Build documentation
	cd docs && make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"