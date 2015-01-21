.PHONY: install uninstall test clean

PREFIX ?= /usr/local

install:
	@cp -f migrate.py $(PREFIX)/bin/migrate

uninstall:
	@rm -f $(PREFIX)/bin/migrate

test:
	@python -m unittest -v test_migrate > /dev/null

clean:
	@rm -fr *.pyc