# Makefile for ShippingMall Logistics Engine

# Environment
VENV_PATH=../../venv
APP_DIR=app
MODULE=app.main:app
RELOAD_DIR=app
PORT=8000
HOST=127.0.0.1

# Run FastAPI server
run:
	source $(VENV_PATH)/bin/activate && \
	uvicorn $(MODULE) --host $(HOST) --port=$(PORT) --reload --reload-dir=$(RELOAD_DIR)

# Format code with black and sort imports
format:
	black $(APP_DIR) && isort $(APP_DIR)

# Run type checks
type-check:
	mypy $(APP_DIR)

# Run tests (extend with pytest if tests are added)
test:
	echo "No tests configured yet."

# Clean Python cache
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
