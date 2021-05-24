.PHONY: docs test help
.DEFAULT_GOAL := help

SHELL := /bin/bash

export ROOTDIR:=$(shell pwd)
export CURRENT_VERSION:=$(shell python3.6 -c "import os; about={}; exec(open(os.path.join('udacity', '_meta.py')).read(), about); print(about['__version__'])")
export CURRENT_USER:=$(shell id -u ${USER}):$(shell id -g ${USER})

# Artifactory configuration (private pypi repository)
export NEXUS_DASNANO_USER:=$(or $(NEXUS_DASNANO_USER), "")
export NEXUS_DASNANO_PASSWORD:=$(or $(NEXUS_DASNANO_PASSWORD), "")
export ARTIFACTORY_URL:=$(or $(ARTIFACTORY_URL), https://nexus.dev.das-nano.com)
export ARTIFACTORY_PIP_URL:=$(or $(ARTIFACTORY_PIP_URL), https://nexus.dev.das-nano.com/repository/pypi-dasnano)
export ARTIFACTORY_APT_URL:=$(or $(ARTIFACTORY_APT_URL), https://nexus.dev.das-nano.com/repository/dasnano-apt/)
export ARTIFACTORY_DOCS_REPOSITORY:=$(or $(ARTIFACTORY_DOCS_REPOSITORY), docs)

# Artifactory configuration for publishing
export ARTIFACTORY_PUB_USER:=$(or $(ARTIFACTORY_PUB_USER), "")
export ARTIFACTORY_PUB_PASSWORD:=$(or $(ARTIFACTORY_PUB_PASSWORD), "")

# Pip configuration
export PIP_EXTRA_INDEX_URL:=$(shell if [ ! -z "${NEXUS_DASNANO_USER}" ]; then echo "${ARTIFACTORY_PIP_URL}" | sed -E 's/^(https?:\/\/)(.*)/\1'${NEXUS_DASNANO_USER}':'${NEXUS_DASNANO_PASSWORD}'@\2/g'; else echo "${ARTIFACTORY_PIP_URL}"; fi)/simple

define PRINT_HELP_PYSCRIPT
import re, sys
print("You can run the following targets (with make <target>): \r\n")
for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"


help:
	@python3.6 -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

# Install/develop

install: ## install the package
	pip install --no-cache-dir $(PIP_ARGS) .

uninstall: ## uninstall the package
	pip uninstall -y $(PIP_ARGS) udacity || true

develop: uninstall ## install the package in development mode
	pip install --editable $(PIP_ARGS) .

# Development

env-create: init-hook ## (re)create a development environment using tox
	tox -e udacity --recreate
	@echo -e "\r\nYou can activate the environment with:\r\n\r\n$$ source ./.tox/udacity/bin/activate\r\n"

env-compile: ## compile requirements.txt / requirements-dev.txt using pip-tools
	pip-compile --no-index --no-header --no-emit-trusted-host --output-file requirements.txt requirements.in
	pip-compile --no-index --no-header --no-emit-trusted-host --output-file requirements-dev.txt requirements-dev.in

env-sync: ## synchornize requirements.txt /requirements-dev.txt with tox virtualenv using pip tools
	pip-sync requirements.txt requirements-dev.txt

env-add-package: ## add new dependency to requirements.in
	@[ "${PACKAGE}" ] || ( echo "PACKAGE is not set"; exit 1 )
	@grep -qxF '${PACKAGE}' requirements.in || echo -e "\n${PACKAGE}" >> requirements.in
	$(MAKE) env-compile
	$(MAKE) env-create
	@echo "Added $(PACKAGE) to requirements.in"

env-add-dev-package: ## add new development dependency to requirements-dev.in
	@[ "${PACKAGE}" ] || ( echo "PACKAGE is not set"; exit 1 )
	@grep -qxF '${PACKAGE}' requirements-dev.in || echo -e "\n${PACKAGE}" >> requirements-dev.in
	$(MAKE) env-compile
	$(MAKE) env-create
	@echo "Added $(PACKAGE) to requirements-dev.in"

env-upgrade-package: ## upgrade the package specified on PACKAGE
	@[ "${PACKAGE}" ] || ( echo "PACKAGE is not set"; exit 1 )
	pip-compile --upgrade-package ${PACKAGE} --no-index --no-header --no-emit-trusted-host --output-file requirements.txt requirements.in

env-upgrade-dev-package: ## upgrade the development package specified on PACKAGE
	@[ "${PACKAGE}" ] || ( echo "PACKAGE is not set"; exit 1 )
	pip-compile --upgrade-package ${PACKAGE} --no-index --no-header --no-emit-trusted-host --output-file requirements-dev.txt requirements-dev.in

env-upgrade-all: ## upgrade all dependencies
	pip-compile --upgrade --no-index --no-header --no-emit-trusted-host --output-file requirements.txt requirements.in
	pip-compile --upgrade --no-index --no-header --no-emit-trusted-host --output-file requirements-dev.txt requirements-dev.in

### QUALITY

lint: ## static code analysis with pylint
	pylint --rcfile udacity/.pylintrc --disable=$(EXTRA_DISABLE) -j 0 udacity
	pylint --rcfile tests/.pylintrc --disable=$(EXTRA_DISABLE) tests

lint-tests: ## static test code analysis with pylint
	pylint --rcfile tests/.pylintrc tests

test: ## run tests with pytest
	py.test

test-report: ## run tests with pytest and generate an HTML report
	py.test --html=docs/_build/test-reports/$(or $(REPORT_NAME), pytest)/index.html \
					--junitxml=docs/_build/test-reports/$(or $(REPORT_NAME), pytest)/junit.xml \
					-o junit_suite_name=$(or $(REPORT_NAME), pytest)

coverage: ## check test coverage
	coverage run --source udacity -m pytest
	coverage report -m --fail-under 90

coverage-report: ## check test coverage and generate an HTML report
	coverage run --source udacity -m pytest
	coverage html
	coverage report -m --fail-under 90

security: ## check source code for vulnerabilities or dangerous code
	bandit -c .bandit.yml -v -r udacity

security-report: ## check source code for vulnerabilities and generate an HTML report
	@mkdir -p docs/_build/security
	bandit -c .bandit.yml -v -r -f html -o docs/_build/security/index.html udacity

check-dependencies: ## check dependencies for vulnerabilities using safety
	safety check --full-report

### FORMAT & DOCS

fmt: ## format code using the PEP8 convention
	black udacity

docs: ## generate project docs
	rm -f docs/udacity.rst
	find docs -name 'udacity.*.rst' -exec rm -f {} +
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ udacity
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/sphinx/html/index.html

diagrams:
	cd docs && \
	./gen_diagrams.sh

raml-docs:
	cd docs && \
	./gen_htmlfromraml.sh

dir-design: pull-daskeleton
	@mkdir -p docs/design
	@cp -n ~/projects/daskeleton/templates/design/index.rst docs/design/index.rst

doc-ad: dir-design
	@cp -n ~/projects/daskeleton/templates/design/ad.rst docs/design/ad.rst
	@echo AD created!

doc-srs: dir-design
	@cp -n ~/projects/daskeleton/templates/design/srs.rst docs/design/srs.rst
	@echo SRS created!

dir-health: pull-daskeleton
	@mkdir -p docs/health
	@cp -n ~/projects/daskeleton/templates/health/index.rst docs/design/index.rst

doc-health-plan: dir-health
	@cp -n ~/projects/daskeleton/templates/health/health_plan.rst docs/health/health_plan.rst
	@echo Health Plan created!

doc-test-plan-log: dir-health
	@cp -n ~/projects/daskeleton/templates/health/test_plan_log.rst docs/health/test_plan_log.rst
	@echo Test Plan Log created!

doc-test-plan-report: dir-health
	@cp -n ~/projects/daskeleton/templates/health/test_plan_report.rst docs/health/test_plan_report.rst
	@echo Test Plan Report created!

doc-test-plan: dir-health
	@cp -n ~/projects/daskeleton/templates/health/test_plan.rst docs/health/test_plan.rst
	@sed -i -e 's/project_name/udacity/g' docs/health/test_plan.rst
	@echo Test Plan created!

dir-operations: pull-daskeleton
	@mkdir -p docs/operations
	@cp -n ~/projects/daskeleton/templates/operations/index.rst docs/operations/index.rst
	@echo Operations created!

doc-build: dir-operations
	@cp -n ~/projects/daskeleton/templates/operations/build.rst docs/operations/build.rst
	@echo Build created!

doc-cfg: dir-operations
	@cp -n ~/projects/daskeleton/templates/operations/configuration.rst docs/operations/configuration.rst
	@echo Configuration created!

doc-deploy: dir-operations
	@cp -n ~/projects/daskeleton/templates/operations/deploy.rst docs/operations/deploy.rst
	@echo Deploy created!

doc-package: dir-operations
	@cp -n ~/projects/daskeleton/templates/operations/package.rst docs/operations/package.rst
	@echo Package created!

doc-provision: dir-operations
	@cp -n ~/projects/daskeleton/templates/operations/provision.rst docs/operations/provision.rst
	@echo Provision created!

doc-release: dir-operations
	@cp -n ~/projects/daskeleton/templates/operations/release.rst docs/operations/release.rst
	@sed -i -e 's/project_name/udacity/g' docs/operations/release.rst
	@echo Release created!

doc-run: dir-operations
	@cp -n ~/projects/daskeleton/templates/operations/run.rst docs/operations/run.rst
	@sed -i -e 's/project_name/udacity/g' docs/operations/run.rst
	@echo Run created!

dir-support: pull-daskeleton
	@mkdir -p docs/support
	@cp -n ~/projects/daskeleton/templates/support/index.rst docs/support/index.rst

doc-usage: dir-support
	@cp -n ~/projects/daskeleton/templates/support/usage.rst docs/support/usage.rst
	@sed -i -e 's/project_name/udacity/g' docs/support/usage.rst
	@sed -i -e 's/project_name/udacity/g' docs/support/usage.rst
	@echo Usage created!

doc-user-manual: dir-support
	@cp -n ~/projects/daskeleton/templates/support/user_manual.rst docs/support/user_manual.rst
	@echo User manual created!

HIGHEST_ADR = $(shell egrep -lr --include=*.rst "adr" docs/design | tr '\n' ' ' | sed -e 's/[^0-9]/ /g' -e 's/^ *//g' -e 's/ *$$//g' | tr -s ' ' | tr ' ' '\n' | sort -n | tail -1 | bc -l)
$(eval HIGHEST_ADR=$(shell echo $$(($(HIGHEST_ADR)+1))))
NEXT_ADR = $(shell printf '%04d' $(HIGHEST_ADR))

doc-adr: dir-design
	@cp -n ~/projects/daskeleton/templates/design/adrs.rst docs/design/adrs.rst
	@cp -n ~/projects/daskeleton/templates/design/adr0000_template.rst docs/design/adr$(NEXT_ADR).rst
	@sed -i -e 's/0000/$(NEXT_ADR)/g' docs/design/adr$(NEXT_ADR).rst
	@echo ADR$(NEXT_FSS) created!

HIGHEST_FSS = $(shell egrep -lr --include=*.rst "fss" docs/design | tr '\n' ' ' | sed -e 's/[^0-9]/ /g' -e 's/^ *//g' -e 's/ *$$//g' | tr -s ' ' | tr ' ' '\n' | sort -n | tail -1 | bc -l)
$(eval HIGHEST_FSS=$(shell echo $$(($(HIGHEST_FSS)+1))))
NEXT_FSS = $(shell printf '%04d' $(HIGHEST_FSS))

doc-fss: dir-design
	@cp -n ~/projects/daskeleton/templates/design/studies.rst docs/design/studies.rst
	@cp -n ~/projects/daskeleton/templates/design/fss0000_template.rst docs/design/fss$(NEXT_FSS).rst
	@sed -i -e 's/0000/$(NEXT_FSS)/g' docs/design/fss$(NEXT_FSS).rst
	@echo FSS$(NEXT_FSS) created!

# Package & Publish

version: ## shows the current package version
	@echo $(CURRENT_VERSION)

# Calculates target version for a tag
ifneq ($(PART),)
TARGET_VERSION := $(shell bump2version --dry-run --allow-dirty --current-version $(CURRENT_VERSION) $(PART) --list | grep new_version= | sed -r s,"^.*=",,)
endif

version-next: ## shows the next version to bump
	@[ "${PART}" ] || ( echo "You must provide which PART of semantic version you want to bump: major.minor.patch"; exit 1 )
	@echo $(TARGET_VERSION)

tag-bump: ## bumps version and creates and commits tag
	@[ "${PART}" ] || ( echo "You must provide which PART of semantic version you want to bump: major.minor.patch"; exit 1 )
	@if [ $(shell if grep -Fq '## $(TARGET_VERSION) ' CHANGELOG.md; then echo "yes"; else echo "no"; fi) = "yes" ];                 \
	then							                                           \
		echo Going to commit tag v$(TARGET_VERSION);                           \
		bump2version  --commit --tag --current-version $(CURRENT_VERSION) $(PART); \
		echo "Please push tag to GitLab with:  ";                                          \
		echo "make tag-push";                                          \
	else		                                                               \
		echo "Tag for v$(TARGET_VERSION) aborted. Please update CHANGELOG.md with the description of changes";   \
	fi

tag-push: ## Pushes tag for current version
	git push origin v$(CURRENT_VERSION)
	git push

tag-delete: ## deletes tag
	git tag -d $(TAG)
	git push --delete origin $(TAG)

dist: clean-build clean-pyc ## build wheel package (compiled)
	python setup.py bdist_wheel --cythonize

dist-dev: clean-build clean-pyc ## build wheel package (source code)
	python setup.py bdist_wheel

sdist: clean-build clean-pyc ## build a source distribution (sdist)
	python setup.py sdist

publish: ## publish packages to the repository
	twine upload -u $(ARTIFACTORY_PUB_USER) -p $(ARTIFACTORY_PUB_PASSWORD) \
		--repository-url $(ARTIFACTORY_PIP_URL)/ \
		--repository $(ARTIFACTORY_PIP_URL)/ \
		dist/udacity*

publish-dev: ## publish packages to the repository.
	@echo "REQUIRES uploader user setup in file ~/.pypirc"
	twine upload --repository dasnano dist/udacity*

publish-apt: ## publish apt package to the repository
	@[ "${PACKAGE}" ] || ( echo "You must provide the PACKAGE location"; exit 1 )
	@curl -u "${NEXUS_DASNANO_USER}:${NEXUS_DASNANO_PASSWORD}" -H "Content-Type: multipart/form-data" \
		--data-binary "@${PACKAGE}" "${ARTIFACTORY_APT_URL}"

publish-from-jetson: ## publish packages to the repository.
	@echo "REQUIRES make nexus-configure or make jetson-configure TO BE RUN ON HOST FIRST"
	pip install twine==3.1.1
	twine upload --repository dasnano dist/udacity*


# Docker

docker-run: ## run the specified command on docker (defaults to /bin/bash)
	docker-compose -f docker/dev/docker-compose.yml run --rm -u $(CURRENT_USER) udacity $(MAKE) $(TARGET)

docker-shell: ## drop the user into a shell inside a docker container
	docker-compose -f docker/dev/docker-compose.yml run --rm -u $(CURRENT_USER) udacity



# Continuous integration

ci-all: # simulate the complete CI pipeline by running all the ci-* targets
	$(MAKE) ci-clean && \
	$(MAKE) ci-prepare && \
	$(MAKE) ci-test && \
	($(MAKE) ci-coverage || true) && \
	($(MAKE) ci-lint || true) && \
	($(MAKE) ci-security || true) && \
	($(MAKE) ci-check-dependencies) && \
	$(MAKE) ci-docs && \
	$(MAKE) ci-dist-dev && \
	$(MAKE) ci-dist

ci-prepare: ci-clean ## prepares the environment to run on CI (GitLab)
	tox -e py36,udacity

ci-lint: ## lint code & tests on CI (GitLab)
	tox -e udacity -- $(MAKE) lint EXTRA_DISABLE=fixme

ci-security: ## checks the source code for known security vulnerabilities (GitLab)
	tox -e udacity -- $(MAKE) security-report

ci-check-dependencies: ## check dependencies for vulnerabilities using safety (GitLab)
	tox -e udacity -- $(MAKE) check-dependencies

ci-test: ## run tests on CI (GitLab)
	tox -e $(or $(ENV_NAME), $(shell echo "py36-test"))

ci-coverage: ## run coverage on CI (GitLab)
	tox -e udacity -- $(MAKE) coverage-report

ci-docs: ## generate docs on CI (GitLab)
	tox -e udacity -- $(MAKE) docs

ci-version-set: ## set the version to the specified VERSION on CI (GitLab)
	tox -e udacity -- $(MAKE) version-set VERSION="${VERSION}"

ci-dist: ## build the package for every supported version on CI (GitLab)
	tox -e py36-dist

ci-dist-dev: ## build the package (for development) for every supported version on CI (GitLab)
	tox -e udacity -- $(MAKE) dist-dev

ci-publish: ## publish built packages to the appropriate repository on CI (GitLab)
	tox -e udacity -- $(MAKE) publish ## publish the packages generated with dist or dist-dev on CI (GitLab)

ci-release: ci-dist ci-publish ## build and publish the package for every supported repository on CI (GitLab)

ci-release-dev: ci-dist-dev ci-publish ## build and publish the package (for development) for every supported repository on CI (GitLab)



ci-clean: clean ## clean workspace on CI (GitLab)

# Cleanup

clean-all: clean clean-env clean-docker ## remove everything (artifacts, environments, etc.)

clean: clean-build clean-dist clean-pyc clean-test clean-docs ## remove all build, test, coverage and Python artifacts

clean-docs: ## remove auto-generated docs
	rm -fr docs/_build

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr .eggs/
	find . ! -path './.tox/*' -name '*.egg-info' -exec rm -fr {} +
	find . ! -path './.tox/*' -name '*.egg' -exec rm -f {} +
	find udacity -name '*.c' -exec rm -f {} +

clean-dist: ## remove dist packages
	rm -fr dist/

clean-pyc: ## remove Python file artifacts
	find . ! -path './.tox/*' -name '*.pyc' -exec rm -f {} +
	find . ! -path './.tox/*' -name '*.pyo' -exec rm -f {} +
	find . ! -path './.tox/*' -name '*~' -exec rm -f {} +
	find . ! -path './.tox/*' -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -rf .pytest_cache
	rm -f .coverage

clean-env: ## remove virtual environments (created by tox)
	rm -fr .tox/

clean-docker: ## remove Docker images, containers, etc.
	docker-compose -f docker/dev/docker-compose.yml down --rmi local --volumes --remove-orphans

# Configure Jetson

# DEVICE can be just IP, include also the port or even user name if differs from host user:
# DEVICE="95.124.245.48"
# DEVICE="-p 31 95.124.245.48"
# DEVICE="-p 31 othername@95.124.245.48"

jetson-configure: git-configure nexus-configure
	@echo "Initializing jetson configuring target"
	@[ "${DEVICE}" ] || ( echo "DEVICE is not set"; exit 1 )
	ssh -p $${PORT:=22} $(DEVICE) "pip3 install pip-tools==5.5.0"
	ssh -p $${PORT:=22} $(DEVICE) "pip3 install cython"
	ssh -p $${PORT:=22} $(DEVICE) "echo 'export PATH=\$$HOME/.local/bin:\$$PATH' >> \$$HOME/.bashrc"
	@echo ""
	@echo "NOTE:"
	@echo "PATH of terminal $(DEVICE) has been updated on ~/.bashrc."
	@echo "To load ~/.bashrc, logout and login terminal again or run source ~/.bashrc !"

git-configure:
	@[ "${DEVICE}" ] || ( echo "DEVICE is not set"; exit 1 )
	$(MAKE) git-lfs-configure
	sudo apt-get install -y xclip
	scp -P $${PORT:=22} ~/.gitconfig $(DEVICE):~/.gitconfig
	ssh -p $${PORT:=22} $(DEVICE) "ssh-keygen -f ~/.ssh/id_rsa -q -N \"\" <<< y >/dev/null && cat ~/.ssh/id_rsa.pub" | xclip -sel clip
	@echo "A new public key of target device has been copied to your clipboard. Paste it in GitLab > Settings > SSH Keys"
	firefox https://gitlab.com/profile/keys &

git-lfs-configure:
	@[ "${DEVICE}" ] || ( echo "DEVICE is not set"; exit 1 )
	ssh -p $${PORT:=22} $(DEVICE) "curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash && sudo apt-get install git-lfs && git lfs install"

nexus-configure:
	@[ "${DEVICE}" ] || ( echo "DEVICE is not set"; exit 1 )
	ssh -p $${PORT:=22} $(DEVICE) "echo 'export NEXUS_DASNANO_USER=$(NEXUS_DASNANO_USER)' >> ~/.bashrc"
	ssh -p $${PORT:=22} $(DEVICE) "echo 'export NEXUS_DASNANO_PASSWORD=$(NEXUS_DASNANO_PASSWORD)' >> ~/.bashrc"
	scp -P $${PORT:=22} ~/.pypirc $(DEVICE):~/.pypirc
	echo "To upload a package to Nexus just run `twine upload -r dasnano dist/*`"


### MISCELANEUOS

init-hook: pull-daskeleton
	cp ~/projects/daskeleton/{{cookiecutter.project_slug}}/prepare-commit-msg .git/hooks/

SKULL := '\xE2\x98\xA0'
MANY_SKULLS := $(SKULL)$(SKULL)$(SKULL)$(SKULL)$(SKULL)$(SKULL)$(SKULL)$(SKULL)$(SKULL)$(SKULL)$(SKULL)$(SKULL)$(SKULL)$(SKULL)$(SKULL)$(SKULL)$(SKULL)$(SKULL)'\n'
pull-daskeleton:
	@printf $(MANY_SKULLS)'GETTING DASKELETON\n'$(MANY_SKULLS)
	@if [ ! -d ~/projects/daskeleton ];                                   \
	then							                                      \
		mkdir -p ~/projects;                                              \
		cd ~/projects;                                                    \
		git clone git@gitlab.com:dasnano/common/templates/daskeleton.git; \
	else		                                                          \
		cd ~/projects/daskeleton;                                         \
		git pull;                                                         \
	fi                                                                    \

### VPN MANAGEMENT

vpn-install: pull-daskeleton ## install the vpn software
	sudo ~/projects/daskeleton/scripts/install_vpn.sh
	echo "Installation completed"

vpn-get-ip: pull-daskeleton ## query terminal ip to vpn
	@[ "${ENVIRONMENT}" ] || ( echo "ENVIRONMENT is not set"; exit 1 )
	@[ "${DEVICE}" ] || ( echo "DEVICE is not set"; exit 2 )
	@[ "${HUB_NAME}" ] || ( echo "HUB_NAME is not set"; exit 3 )
	python3 ~/projects/daskeleton/scripts/query_vpn.py -environment=${ENVIRONMENT} -hubname=${HUB_NAME} -terminal=${DEVICE}

vpn-configure: pull-daskeleton enable-sudo ## connect to terminal through vpn
	@[ "${ENVIRONMENT}" ] || ( echo "ENVIRONMENT is not set"; exit 2 )
	@[ "${HUB_NAME}" ] || ( echo "HUB_NAME is not set"; exit 3 )
	~/projects/daskeleton/scripts/configure_vpn.sh ENVIRONMENT=${ENVIRONMENT} HUB_NAME=${HUB_NAME}

vpn-connect: vpn-configure ## connect to terminal through vpn
	@[ "${DEVICE}" ] || ( echo "DEVICE is not set"; exit 1 )
	ssh -p $${PORT:=22} $(DEVICE)

enable-sudo:
	@sudo echo "sudo enabled"
