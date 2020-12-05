.PHONY: test test_lib test_test_project package test_package uploadcodecov

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

uploadcodecov:
	curl -s https://codecov.io/bash > codecov && chmod +x codecov
	./codecov -f ./test_project/coverage.xml -F test_project
	./codecov -f ./.coverage -F test_lib
