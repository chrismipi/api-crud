tests: unit_test coverage

coverage:
	coverage run -m unittest discover -s ./tests && coverage report -m

unit_test:
	python -m unittest discover -v ./tests