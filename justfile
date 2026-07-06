install:
    python -m pip install -e ".[dev]"

run:
    PYTHONPATH=src python -m consent_input_lab.app

test:
    PYTHONPATH=src pytest

lint:
    ruff check .

format:
    ruff format .
