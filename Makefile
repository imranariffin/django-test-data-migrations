.PHONY: test test_lib test_test_project package test_package

test_test_project:
	cd ./test_project && \
		poetry run ./manage.py test \
			-v 2 \
			--noinput \
			--with-coverage \
			--with-xunit \
			--xunit-file coverage.xml

test_lib:
	coverage run --source=tests -m unittest discover tests -v

package:
	poetry check
	poetry run pip check
	poetry run safety check --bare --full-report

test: test_lib test_test_project

test_package: test package
