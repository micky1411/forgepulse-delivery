.PHONY: setup test lint build local-up local-down helm-check terraform-check
setup:
	python -m pip install -e ".[dev]"
test:
	python -m pytest -q
lint:
	python -m ruff check .
build:
	docker build -t forgepulse:local .
local-up:
	docker compose up -d --build
local-down:
	docker compose down
helm-check:
	helm lint helm/forgepulse
terraform-check:
	terraform -chdir=terraform/environments/dev fmt -check -recursive
	terraform -chdir=terraform/environments/dev validate
