test:
	py.test --cov tinysqs --cov-report=term-missing -vsrx tinysqs

clean-pycache:
	find -type d -name __pycache__ | xargs rm -r
