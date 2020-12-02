.PHONY: test package test_package

test:
	cd ./test_project \
	  && poetry run ./manage.py test\
	 	 -v 2 --noinput \
		 --with-coverage \
		 --with-xunit \
		 --xunit-file coverage.xml

package:
	poetry check
	poetry run pip check
	poetry run safety check --bare --full-report

test_package: test package
