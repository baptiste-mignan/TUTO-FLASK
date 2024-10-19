.PHONY: run
run:
	bash -c "source venv/bin/activate && flask run"

.PHONY: install
install:
	virtualenv -p python3 venv
	bash -c "source venv/bin/activate && pip install -r requirement.txt"

.PHONY: loaddb
loaddb:
	bash -c "source venv/bin/activate && flask loaddb ./tuto/data.yml"

