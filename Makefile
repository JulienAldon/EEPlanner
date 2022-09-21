PIP = pip
PYTHON = pipenv run python

.DEFAULT: usage

usage:
		@echo "Usage:"
		@echo "    make build           # Build source distribution archives"
		@echo "    make deploy_prod     # Upload source distribution archives to pypi.org"
		@echo "    make deploy_test     # Upload source distribution archives to test.pypi.org"

install:
		$(PYTHON) --version
		$(PIP) install .[dev]
		xdg-icon-resource install --size 128 assets/application-eeplanner.png
		desktop-file-install --dir=$$HOME/.local/share/applications eeplanner.desktop	

build:
		rm -rf dist && $(PYTHON) setup.py sdist bdist_wheel

deploy_test:
		twine upload -r pypitest dist/*

deploy_prod:
		twine upload -r pypi dist/*

.PHONY: usage install build deploy_test deploy_prod