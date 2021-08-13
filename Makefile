.PHONY: ship test

ship:
	python setup.py sdist bdist_wheel
	twine upload dist/* --skip-existing

lint:
	flake8 yamlfield

test:
	coverage run setup.py test
	coverage report -m
