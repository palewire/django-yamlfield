.PHONY: ship test

ship:
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload dist/* --skip-existing

lint:
	pipenv run flake8 yamlfield

test:
	pipenv run coverage run setup.py test
	pipenv run coverage report -m
