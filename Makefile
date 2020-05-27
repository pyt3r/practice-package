PACKAGE_NAME=template
PACKAGE_PATH=`python -c "import ${PACKAGE_NAME}, os; print(os.path.dirname(${PACKAGE_NAME}.__file__))"`
PYVERSION=3.7

test-env:
	conda env create --name test-env-${PACKAGE_NAME} --file ci/test-env-requirements.yml python=${PYVERSION}

remove-test-env:
	conda env remove --name test-env-${PACKAGE_NAME}

rtd-env:
	conda env create --file ci/rtd-env-requirements.yml python=${PYVERSION}

_pip-env:
	python -m venv pip-env
	echo '' && \
	echo ' # to activate:' && \
	echo ' #    > source pip-env/bin/activate' && \
	echo ' # to deactivate:' && \
	echo ' #    > deactivate' && \
	echo ''

pep8:
	python -m autopep8 ${PACKAGE_NAME}/ -a -r --in-place

lint:
	python -m flake8 ${PACKAGE_NAME}/ --count --show-source --statistics

test:
	coverage run -m unittest discover tests
	coverage report -m
	coverage html
	coverage xml
	open htmlcov/index.html

conda-package:
	conda build . --output-folder=./
	conda install ./**/*.tar.bz2

test-package:
	cd tests && \
	coverage run -m --source=${PACKAGE_PATH} unittest discover . && \
	coverage report -m && \
	coverage html && \
	coverage xml && \
	conda uninstall ${PACKAGE_NAME} -y --force && \
	cd ..

docs-html:
	cd docs/ && \
	make html && \
	open build/html/index.html && \
	cd ..

docs-pdf:
	sphinx-build -b pdf docs/source docs/build
	open docs/build/${PACKAGE_NAME}.pdf

docs-latex:
	cd docs/ && \
	make latexpdf && \
	cd ..

clean:
	rm -rf .coverage htmlcov coverage.xml tests/.coverage tests/htmlcov tests/coverage.xml
	rm -rf channeldata.json index.html noarch osx-64 linux-32 linux-64 win-32 win-64 icons
	find . -name "__pycache__" | xargs  rm -rf
	find . -name "*.pyc" | xargs rm -rf
	rm -rf docs/build/ docs/source/examples

.PHONY: test-env remove-test-env rtd-env _pip-env add-packages pep8 lint test conda-package test-package docs-html docs-pdf docs-latex clean
