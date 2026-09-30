# Local development. Every target runs from the repository root.
.PHONY: up down logs migrate seed test lint typecheck dev-api dev-web lock diagram \
        aws-bootstrap infra-plan infra-apply deploy rollback

BACKEND := cd backend &&
VENV := .venv/bin

up:            ## build and start Postgres, Redis, API, Celery worker/beat, web
	cp -n .env.example .env 2>/dev/null || true
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f backend celery-worker celery-beat frontend

migrate:
	docker compose exec backend python manage.py migrate

seed:          ## demo care team, patients, a signed encounter, a pending AI draft
	docker compose exec backend python manage.py seed_demo

test:          ## backend + frontend tests
	$(BACKEND) $(VENV)/pytest --cov=apps -q
	cd frontend && npm run test:unit

lint:
	$(BACKEND) $(VENV)/ruff check .
	cd frontend && npm run lint

typecheck:
	$(BACKEND) $(VENV)/mypy apps config
	cd frontend && npx vue-tsc --noEmit

dev-api:       ## API with reload against local Postgres/Redis (backend/.env)
	$(BACKEND) $(VENV)/python manage.py runserver 8000

dev-web:
	cd frontend && npm run dev

lock:          ## re-pin backend runtime dependencies
	$(BACKEND) python3 -m venv /tmp/carepath-relock && /tmp/carepath-relock/bin/pip install -q . && /tmp/carepath-relock/bin/pip freeze > requirements.txt

diagram:
	python3 docs/architecture/gen_aws_diagram.py --png && python3 docs/architecture/gen_business_flows.py --png

# ── AWS (plan §15). ENV=staging|prod ──
aws-bootstrap: ## once per account: Terraform state bucket + backend.hcl
	scripts/aws/bootstrap.sh

infra-plan:
	scripts/aws/infra.sh plan $(ENV)

infra-apply:
	scripts/aws/infra.sh apply $(ENV)

deploy:        ## build → push → migrate → release → smoke test
	scripts/aws/deploy.sh $(ENV) $(TAG)

rollback:
	scripts/aws/rollback.sh $(ENV) $(SERVICE)
