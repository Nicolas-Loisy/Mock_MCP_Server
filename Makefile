VENV := .venv
PYTHON := $(VENV)/Scripts/python.exe
PIP := $(VENV)/Scripts/pip.exe

IMAGE := mock-mcp-server

.PHONY: venv install start clean docker-build docker-run

venv:
	test -f $(PYTHON) || python -m venv $(VENV)

install: venv
	$(PIP) install -r requirements.txt

start:
	$(PYTHON) server.py

clean:
	rm -rf $(VENV) __pycache__

docker-build:
	docker build -t $(IMAGE) .

docker-run: docker-build
	docker run --rm -p 8000:8000 $(IMAGE)
