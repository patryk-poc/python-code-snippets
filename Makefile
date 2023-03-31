.PHONY: help clean build

.DEFAULT_GOAL := help

help: check-os
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

include $(if $(wildcard .env),.env)

# Project setup helper tasks
check-os:
	@if [ "$(shell uname -s)" != "Darwin" ]; then echo "Error: Only MAC OS is supported now"; exit 1; fi

# Hooks
disable-hooks:
	@git config --global --unset core.hooksPath || true
	@git config --global --unset hooks.gitleaks || true
	@git config --local --unset core.hooksPath || true
	@if [ -f .git/hooks/pre-commit ]; then rm .git/hooks/pre-commit; fi

install-hooks: disable-hooks
	@poetry run pre-commit install
	@git config --global hooks.gitleaks true
	@git config --global core.hooksPath $(HOME)/.GitClientHooks
	@git config --local core.hooksPath .git/hooks

update-hooks: ## Auto-update pre-commit config to the latest repos' versions
	@poetry run pre-commit autoupdate

install: install-hooks ## Install tools
	@poetry install

# Tests
test: ## Run unit tests
	@poetry run pytest
