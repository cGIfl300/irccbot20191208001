all: clean init doc setup pycache

init:
	@echo "Entering setup"
	@echo "Generating virtual environment"
	virtualenv -p python3 venv
	venv/bin/python3 -m pip install -r requierements.txt

clean:
	@echo "Entering clean"
	@echo "Cleaning"
	rm -rvf __pycache__
	rm -rvf venv

pycache:
	@echo "Removing __pycache__"
	rm -rvf __pycache
