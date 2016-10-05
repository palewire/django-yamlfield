.PHONY: test

test:
	flake8 yamlfield
	coverage run setup.py test
