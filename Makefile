.PHONY: help clean build

.DEFAULT_GOAL := help

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

include $(if $(wildcard .env),.env)

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

install-with-hooks: install-hooks install ## Install with hooks for local dev only

install: ## Install tools
	@poetry install --no-root

# Tests
test-clean:
	@rm -rf .coverage .pytest_cache 2>/dev/null

test: test-clean ## Run unit tests
	@poetry run pytest
