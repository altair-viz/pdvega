all:
	install

install:
	python setup.py install

test:
	python -m pytest --pyargs --doctest-modules pdvega

test-coverage:
	python -m pytest --pyargs --doctest-modules --cov=pdvega --cov-report term pdvega

test-coverage-html:
	python -m pytest --pyargs --doctest-modules --cov=pdvega --cov-report html pdvega
