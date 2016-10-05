.PHONY: ship test

ship:
	python setup.py sdist bdist_wheel
	twine upload dist/* --skip-existing

test:
	flake8 yamlfield
	coverage run setup.py test
