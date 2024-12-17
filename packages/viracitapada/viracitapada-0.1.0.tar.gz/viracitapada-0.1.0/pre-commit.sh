!#!/usr/bin/env sh

# Format code and fix linter errors
uv run ruff format .
uv run ruff check . --fix

# Check code formatting, run linter
uv run ruff format . --check
uv run ruff check .

# run mypy
uv run mypy

# Run tests and measure test coverage
uv run coverage run -m pytest

# Print coverage report of last measured test run
uv run coverage report -m
