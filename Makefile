.PHONY: test exact ideal noisy figures paper clean install

install:
	pip install -e '.[all]'

test:
	pytest tests/ -v

exact:
	python -c "from tests.run_exact import main; main()"

ideal:
	python -c "from experiments.ideal.run_ideal import main; main()"

noisy:
	python -c "from experiments.noisy.run_noisy import main; main()"

figures:
	python -c "from analysis.generate_figures import main; main()"

paper:
	cd paper && pdflatex main.tex

clean:
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf .pytest_cache
	rm -rf *.pyc
	rm -rf results/*.json
