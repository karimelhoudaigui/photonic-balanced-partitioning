PYTHON ?= .venv/bin/python
TECTONIC ?= tectonic
.PHONY: test figures paper check install clean offline-pilot
install:
	$(PYTHON) -m pip install -e '.[all]'
test:
	OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 $(PYTHON) -m pytest tests/ -q
figures:
	$(PYTHON) scripts/build_publication.py
check:
	$(PYTHON) scripts/build_publication.py --check
paper: check
	$(TECTONIC) --untrusted --keep-logs paper/main.tex
	$(PYTHON) scripts/verify_manuscript.py
# The destination must be new; provide OUT=/absolute/new/directory.
offline-pilot:
	@test -n "$(OUT)" || (echo 'Set OUT to a new directory'; exit 2)
	PYTHONPATH=src OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 $(PYTHON) qpu/offline_pilot_20261124_v1/reproduce.py --output "$(OUT)"
clean:
	$(PYTHON) scripts/clean_build.py
