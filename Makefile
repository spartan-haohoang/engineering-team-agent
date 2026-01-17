.PHONY: help install run docker-build docker-up docker-down docker-logs docker-restart clean setup test test-cov format lint

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Initial setup - create .env from example
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "Created .env file. Please edit it with your API keys."; \
	else \
		echo ".env file already exists."; \
	fi
	@echo "Make sure to set:"
	@echo "  - OPENAI_API_KEY"
	@echo "  - ANTHROPIC_API_KEY"

install: ## Install dependencies using uv
	uv sync

install-dev: ## Install dependencies with dev tools
	uv sync --dev

run: ## Run the application locally
	uv run streamlit run src/engineering_team_agent/app.py

test: ## Run tests
	uv run pytest

test-cov: ## Run tests with coverage
	uv run pytest --cov

test-unit: ## Run only unit tests
	uv run pytest -m unit

test-integration: ## Run only integration tests
	uv run pytest -m integration

format: ## Format code with black
	uv run black src/ tests/

lint: ## Lint code with ruff
	uv run ruff check src/ tests/

docker-build: ## Build Docker image
	docker-compose build

docker-up: ## Start Docker container
	docker-compose up -d

docker-down: ## Stop Docker container
	docker-compose down

docker-logs: ## View Docker logs
	docker-compose logs -f

docker-restart: ## Restart Docker container
	docker-compose restart

clean: ## Clean Python cache and build files
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true
	rm -rf build/ dist/ .pytest_cache/ .coverage htmlcov/ .coverage.*
	rm -rf output/*.py output/*.md output/*.txt 2>/dev/null || true
