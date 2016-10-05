.PHONY: test

test:
	pep8 yamlfield
	pyflakes yamlfield
	coverage run setup.py test
