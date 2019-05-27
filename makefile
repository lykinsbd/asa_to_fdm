# The version of the container will be the name of the most recent git tag. Before building a new container,
# please tag the repo with the new version number.
version = $(shell git for-each-ref --sort=-taggerdate --format '%(refname:short)' refs/tags | head -n 1)
tarball = dist/asa_to_fdm-$(version).tar.gz

.PHONY: all
all: help

.PHONY: clean
clean: docclean  ## Delete temporary files
	-rm -rf dist build .eggs asa_to_fdm.egg-info .tox .coverage htmlcov coverage.xml .config share version
	-find asa_to_fdm -name __pycache__ -exec rm -rf "{}" \;
	-find asa_to_fdm -name '*.pyc' -exec rm -f "{}" \;

.PHONY: docclean
docclean:  ## Delete cached documentation to avoid a lot of bugs in Sphinx. Especially required for sphinx_selective_exclude
	-find . -name .doctrees -exec rm -rf "{}" \;

.PHONY: distclean
distclean: clean  ## Delete anything that's not part of the repo
	git reset HEAD --hard
	git clean -fxd

.PHONY: dist
dist:  ## Create the Tarball of this code
	@echo Creating tarball
	python setup.py sdist bdist_wheel

.PHONY: container
container:  ## Build the container for deployment
	@echo Checking for untagged changes...
	test -z "$(shell git status --porcelain)"
	git diff-index --quiet $(version)
	@echo Repo is clean.
	@echo Building container...
	docker build --pull \
	--build-arg version="$(version)" \
	--build-arg tarball="$(tarball)"
	--tag lykinsbd/asa_to_fdm:$(version) \
	--tag lykinsbd/asa_to_fdm:latest .

.PHONY: push
push:  ## Push container to Docker Hub
	@echo Pushing to Docker Hub
	docker push lykinsbd/asa_to_fdm:$(version)
	docker push lykinsbd/asa_to_fdm:latest

.PHONY: banner
banner:
	@echo '  ___   _____  ___    _         _______________  ___'
	@echo ' / _ \ /  ___|/ _ \  | |        |  ___|  _  \  \/  |'
	@echo '/ /_\ \\ `--./ /_\ \ | |_ ___   | |_  | | | | .  . |'
	@echo '|  _  | `--. \  _  | | __/ _ \  |  _| | | | | |\/| |'
	@echo '| | | |/\__/ / | | | | || (_) | | |   | |/ /| |  | |'
	@echo '\_| |_/\____/\_| |_/  \__\___/  \_|   |___/ \_|  |_/'
	@echo ''

.PHONY: help
help: banner
# Help function shamelessly stolen from the Rackspace Engineering Handbook
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
