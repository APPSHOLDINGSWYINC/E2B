.PHONY: help install test clean example

help:
	@echo "AgentX5 Multi-Dump Parser - Available targets:"
	@echo "  install    Install dependencies"
	@echo "  test       Run tests"
	@echo "  example    Run parser with example data"
	@echo "  clean      Clean generated files"

install:
	pip install -r requirements.txt

test:
	python -m pytest test_multi_dump_parser.py -v

example:
	python multi_dump_parser.py example_dump.txt example_output
	@echo "\nGenerated files:"
	@ls -lh example_output/

clean:
	rm -rf __pycache__ .pytest_cache .coverage htmlcov
	rm -rf example_output test_output
	rm -rf build dist *.egg-info
