PYTEST?=python3 -m pytest

test:
	${PYTEST} -s -v tests

coverage:
	SHORT_TESTS=1 ${PYTEST} -s -vv --cov-report=html --cov=ponyparser tests

stdlib_coverage:
	${PYTEST} -s -vv --cov-report=html --cov=ponyparser tests

.PHONY: test coverage
