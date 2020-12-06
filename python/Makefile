
:PHONY clean build test

clean: 
	-rm *.pyc
	-rm *.zip

sub:
	../apr/secret/remove_sensitive.sh . sub
res:
	../apr/secret/remove_sensitive.sh . res

install:
	pip install -r requirements.txt

env: 
	-virtualenv venv --python=python3.9

activate:
	source venv/bin/activate

deactivate:
	deactivate

rmenv:
	rm -rf venv

config: env activate install

test:
	python test.py
	python test_api.py
	python test_api_wrapper.py
