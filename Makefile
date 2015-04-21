
install:
	@python setup.py install
	@make clean

uninstall:
	@pip uninstall migrate

test:
	@python -m unittest -v test_migrate > /dev/null

clean:
	@rm -fr *.pyc build dist migrate.egg-info

upload:
	@python setup.py sdist upload -r pypi
	@make clean

.PHONY: install uninstall test clean
