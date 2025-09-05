.PHONY: up down reset logs ui pg-init status help

# Start all services
up:
	docker compose up -d

# Stop all services
down:
	docker compose down

# Reset environment (drop volumes and recreate containers)
reset:
	docker compose down -v
	docker compose up -d

# Stream logs from containers
logs:
	docker compose logs -f

# Show access URLs
ui:
	@echo "Airflow UI: http://localhost:8080"
	@echo "MinIO Console: http://localhost:9001"

# Initialize warehouse PostgreSQL with a sample table and data

pg-init:
	docker compose exec -T warehouse-pg psql -U analytics -d analytics -c "\
	CREATE TABLE IF NOT EXISTS raw_jsonplaceholder_posts (id INTEGER PRIMARY KEY, user_id INTEGER, title TEXT, body TEXT, payload JSONB, ingested_at TIMESTAMPTZ DEFAULT now()); \
	INSERT INTO raw_jsonplaceholder_posts (id, user_id, title, body, payload) VALUES (1,1,'hello','from pg-init','{\"hello\":\"world\"}') ON CONFLICT(id) DO NOTHING;"

show-password:
	docker compose exec airflow-api bash -lc 'echo "Password for admin:"; cat "$$AIRFLOW_HOME/simple_auth_manager_passwords.json.generated"'

# Show container statuses
status:
	docker compose ps

# Display help with available targets
help:
	@grep -E '^[a-zA-Z_-]+:.*?##' Makefile | awk -F ':' '{printf "  %-12s %s\n", $$1, $$2}'
