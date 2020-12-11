
:PHONY clean build test

clean: 
	-rm *.pyc
	-rm *.zip
	-rm -rf build
	-rm -rf dist
	-rm -rf *.egg-info

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


setup:
	python setup.py build
	python setup.py sdist
	pip install dist/*.tar.gz