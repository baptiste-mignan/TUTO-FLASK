.PHONY: install
install:
	virtualenv -p python3 venv
	bash -c "source venv/bin/activate && pip install -r requirement.txt"
