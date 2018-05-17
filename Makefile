TOX = tox
PYTEST_OPTS =

JULIA = julia

JULIA_PYTHON = $(shell $(JULIA) -e 'print(readstring(Pkg.dir("PyCall", "deps", "PYTHON")))')

SSL_CERT_FILE = $(shell $(JULIA) -e 'print(joinpath(JULIA_HOME, Base.DATAROOTDIR, "julia", "cert.pem"))')
export SSL_CERT_FILE

.PHONY: test*

test-notox:
	$(JULIA_PYTHON) -m pytest src $(PYTEST_OPTS)

test-tox:
	$(TOX) -- $(PYTEST_OPTS)
