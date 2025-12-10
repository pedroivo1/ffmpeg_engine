.PHONY: test-unit
.PHONY: test-ordered
.PHONY: test-global-options

test-unit:
	python -m pytest tests/unit/

test-ordered:
	python -m pytest tests/unit/test_flags.py tests/unit/test_builders.py tests/unit/test_runner.py

test-global-options:
	python -m pytest .\tests\unit\options\test_global_options.py
