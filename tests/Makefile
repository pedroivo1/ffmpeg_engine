.PHONY: test-unit
.PHONY: test-ordered

# Comando para rodar todos os testes de unidade (unit)
test-unit:
	python -m pytest tests/unit/

# Comando para rodar os testes na ordem específica de dependência
test-ordered:
	python -m pytest tests/unit/test_flags.py tests/unit/test_builders.py tests/unit/test_runner.py
