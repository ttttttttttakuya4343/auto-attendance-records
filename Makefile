.PHONY: help install test lint format clean run

help:
	@echo "Available commands:"
	@echo "  install    - Install dependencies"
	@echo "  test       - Run tests"
	@echo "  lint       - Run linting"
	@echo "  format     - Format code"
	@echo "  clean      - Clean build artifacts"
	@echo "  run        - Run the application"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	python tests/run_all_tests.py

lint:
	@command -v flake8 >/dev/null 2>&1 || { echo "flake8 not installed. Run 'make install-dev' first."; exit 1; }
	@command -v mypy >/dev/null 2>&1 || { echo "mypy not installed. Run 'make install-dev' first."; exit 1; }
	flake8 src apps tests
	mypy src apps

format:
	@command -v black >/dev/null 2>&1 || { echo "black not installed. Run 'make install-dev' first."; exit 1; }
	black src apps tests

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf build/ dist/ *.egg-info/

run:
	python run.py