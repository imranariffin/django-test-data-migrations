.PHONY: test test_lib test_test_project test_package publish

test_test_project:
	cd ./test_project && \
		poetry run ./manage.py test \
			-v 2 \
			--noinput \
			--with-coverage \
			--with-xunit \
			--xunit-file coverage.xml

test_lib:
	poetry run coverage run --source=tests -m unittest discover tests -v

test_package:
	poetry check
	poetry run pip check

test: test_lib test_test_project test_package

publish:
	poetry run twine upload \
		--skip-existing \
		--verbose \
		--repository ${PYPI_REPOSITORY} \
		--username __token__ \
		--password ${PYPI_API_TOKEN} \
		./dist/*
