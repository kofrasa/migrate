
install:
	@python setup.py install
	@make clean

uninstall:
	@pip uninstall migrate

test:
	@python -m unittest -v test_migrate > /dev/null

clean:
	@rm -fr *.pyc build dist migrate.egg-info

.PHONY: install uninstall test clean