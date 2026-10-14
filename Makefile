.PHONY: check up dbt test token psql down

check:  ## Verify Docker is available and the images build
	docker compose version
	docker compose build
	@echo "Environment OK"

up:  ## Start Postgres, load seeds, build dbt models, start the API on :8000
	docker compose up -d postgres
	docker compose run --rm dbt build
	docker compose up -d api

dbt:  ## Run any dbt command, e.g. make dbt CMD="build -s mart_symptom_answer"
	docker compose run --rm dbt $(or $(CMD),build)

test:  ## Run the API test suite
	docker compose run --rm --no-deps api pytest -q

token:  ## Issue a dev token, e.g. make token STUDIES="ONC-101"
	@docker compose run --rm --no-deps api python scripts/make_token.py --sub researcher@example.org --studies $(STUDIES)

psql:  ## Open a SQL shell
	docker compose exec postgres psql -U rdp -d rdp

down:
	docker compose down -v
