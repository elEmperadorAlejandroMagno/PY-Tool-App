VENV?=.venv
PYTHON?=$(VENV)/bin/python
PIP?=$(VENV)/bin/pip

.PHONY: venv install run clean

venv:
	python3 -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) app.py

clean:
	rm -rf $(VENV) __pycache__ **/__pycache__ .pytest_cache .mypy_cache
