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

# Show container statuses
status:
	docker compose ps

# Display help with available targets
help:
	@grep -E '^[a-zA-Z_-]+:.*?##' Makefile | awk -F ':' '{printf "  %-12s %s\n", $$1, $$2}'
