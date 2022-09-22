PACKAGES=$(shell grep -E '(my_common|^aioworkers)' Pipfile | sed -r 's/([-a-z]+) = (.*)\"(.*)\".*/\1\3/')
export PIP_CONFIG_FILE=$(shell pwd)/setup.cfg


.PHONY: deps, run_server, test, clean


deps:
	pip install -r ./requirements.txt --isolated

migrate:
	python src/cubicon/manage.py migrate

run_server:
	python src/cubicon/manage.py runserver 0.0.0.0:80

lint: mypy flake

mypy:
	@mypy src tests

flake:
	@flake8 scr tests

#test:
#	./runtests.py
#	@pytest tests

ci-test:
	@pytest --junit-xml=$(JUNITXML) --cov=src/cubicon --cov-report=html

clean:
	rm -r build dist
	@rm -rf `find . -name __pycache__`
	@rm -f `find . -type f -name '*.py[co]'`
# 	@python setup.py clean
#	@rm -f .make-*
	@rm -rf *.egg-info
	@rm -f Pipfile.lock poetry.lock

cubicon/version.py:
	echo "__version__ = '$(shell git describe --tags --always)'" > $@

requirements.txt:
	pipenv lock --requirements | grep -v '\-i http' > requirements.txt

merge_to_test1:
	$(MAKE) .merge_to_test1 BRANCH=$(shell git rev-parse --abbrev-ref HEAD)

.merge_to_test1:
	git stash
	git checkout test1
	git pull
	git merge $(BRANCH)
	git push origin test1
	git checkout $(BRANCH)
	git stash pop