.Phony install
install:
	virtualenv -p -python3 virtualenv
	source venv/bin/activate
	pip install -r ./requirement.txt
