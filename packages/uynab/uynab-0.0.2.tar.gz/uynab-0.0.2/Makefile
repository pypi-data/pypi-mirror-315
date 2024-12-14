.PHONY: setup check-uv build test clean clean_venv clean_build clean_cache lint docs

setup: check-uv uv.lock
	@echo "Setting up projcet..."
	uv sync

	
check-uv:
	@if ! command -v uv > /dev/null; then \
		echo "UV is not installed"; \
		echo "Installing UV"; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	fi

build: test
	@echo "Building package..."
	uv build

test: test/test_*.py
	@echo "Running tests..."
	@if ! uv run pytest; then \
		echo "Tests failed. Building project not possible."; \
		exit 1; \
	fi

clean: clean_venv clean_build clean_cache

clean_venv:
	@echo "Removing virtual environment.."
	rm -rf .venv

clean_build:
	@echo "Removing build files..."
	rm -rf dist/

clean_cache:
	@echo "Removing all cache files and directories int the project..." 
	find . -name "*cache*" -type d | xargs -t -I {} rm -rf "{}"

lint:
	@echo "Formatting project files with ruff..."
	uv run ruff format

docs_serve: docs
	uv run mkdocs serve

docs:
	uv run mkdocs build
