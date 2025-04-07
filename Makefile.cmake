.PHONY: install test clean lint format build docker-build

# Default Python interpreter
PYTHON = python3

# Install basic version
install:
	$(PYTHON) -m pip install -e .

# Install with Celery support
celery-install:
	$(PYTHON) -m pip install -e ".[celery]"

# Install dev dependencies
dev-install:
	$(PYTHON) -m pip install -e ".[dev]"

# Install all dependencies
all-install:
	$(PYTHON) -m pip install -e ".[all]"

# Run tests
test:
	$(PYTHON) -m pytest tests/

# Run tests with coverage
test-cov:
	$(PYTHON) -m pytest --cov=pasture tests/ --cov-report=term --cov-report=html

# Clean build artifacts
clean:
	rm -rf build/ dist/ *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name "*.eggs" -exec rm -rf {} +
	find . -type d -name "*.pytest_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +

# Format code
format:
	$(PYTHON) -m black pasture/ tests/ examples/
	$(PYTHON) -m isort pasture/ tests/ examples/

# Lint code
lint:
	$(PYTHON) -m black --check pasture/ tests/ examples/
	$(PYTHON) -m isort --check pasture/ tests/ examples/
	$(PYTHON) -m mypy pasture/

# Build package
build: clean
	$(PYTHON) -m pip install --upgrade build
	$(PYTHON) -m build

# Build Docker image
docker-build:
	docker build -t pasture:latest .

# Run example in Docker
docker-run:
	docker run --rm -it \
		-v $(PWD)/config:/app/config \
		-v $(PWD)/cache:/app/cache \
		pasture:latest

# Run example
run-example:
	$(PYTHON) examples/simple_pipeline.py

# Run multi-model example
run-multi-example:
	$(PYTHON) examples/multi_model.py

# Run Celery example (requires Redis)
run-celery-example:
	$(PYTHON) examples/celery_pipeline.py

# Start Celery worker for examples
start-worker:
	celery -A examples.celery_pipeline worker --loglevel=info
