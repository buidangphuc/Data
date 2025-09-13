# ========= MinIO bucket helper =========

# ========= MinIO credentials =========
AWS_ACCESS_KEY_ID ?= minio
AWS_SECRET_ACCESS_KEY ?= minio12345

MINIO_HOST ?= minio
MINIO_PORT ?= 9000
MINIO_BUCKET ?= warehouse

.PHONY: minio-bucket
minio-bucket:
	@if [ -z "$${AWS_ACCESS_KEY_ID}" ] || [ -z "$${AWS_SECRET_ACCESS_KEY}" ]; then \
	  echo "Missing credentials. Export AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY first."; \
	  echo "   e.g.: export AWS_ACCESS_KEY_ID=minioadmin ; export AWS_SECRET_ACCESS_KEY=minioadmin"; \
	  exit 1; \
	fi
	@echo "Finding Docker network of service $(MINIO_HOST)..."
	@NET=$$(docker inspect -f '{{range $$k,$$v := .NetworkSettings.Networks}}{{$$k}}{{end}}' $$(docker compose ps -q $(MINIO_HOST))); \
	  if [ -z "$$NET" ]; then \
	    echo "Container '$(MINIO_HOST)' not found. Make sure docker compose is up and service name is correct."; \
	    exit 1; \
	  fi; \
	  echo "Network: $$NET"; \
	  echo "Creating bucket '$(MINIO_BUCKET)' on http://$(MINIO_HOST):$(MINIO_PORT) ..."; \
	  docker run --rm --network $$NET \
	    -e MC_HOST_myminio=http://$${AWS_ACCESS_KEY_ID}:$${AWS_SECRET_ACCESS_KEY}@$(MINIO_HOST):$(MINIO_PORT) \
	    minio/mc mb --ignore-existing myminio/$(MINIO_BUCKET); \
	  echo "Creating prefix iceberg/ (if not exists)"; \
	  docker run --rm --network $$NET \
	    -e MC_HOST_myminio=http://$${AWS_ACCESS_KEY_ID}:$${AWS_SECRET_ACCESS_KEY}@$(MINIO_HOST):$(MINIO_PORT) \
	    minio/mc cp /dev/null myminio/$(MINIO_BUCKET)/iceberg/.keep >/dev/null 2>&1 || true; \
	  echo "Listing bucket:"; \
	  docker run --rm --network $$NET \
	    -e MC_HOST_myminio=http://$${AWS_ACCESS_KEY_ID}:$${AWS_SECRET_ACCESS_KEY}@$(MINIO_HOST):$(MINIO_PORT) \
	    minio/mc ls myminio/$(MINIO_BUCKET)
.PHONY: up down nuke logs topics topics-reset seed flink-sql spark-job

# Start all services
up:
	docker compose up -d --build

# Stop all services
down:
	docker compose down

# Remove all containers, volumes, and local images
nuke:
	docker compose down -v --rmi local

# Tail logs from all services
logs:
	docker compose logs -f

# Create Kafka topic
topics:
	- docker compose exec -T kafka kafka-topics.sh --create \
		--topic events.raw --bootstrap-server kafka:9092 \
		--partitions 1 --replication-factor 1

# Delete and recreate Kafka topic
topics-reset:
	- docker compose exec -T kafka kafka-topics.sh --delete \
		--topic events.raw --bootstrap-server kafka:9092
	sleep 2
	docker compose exec -T kafka kafka-topics.sh --create \
		--topic events.raw --bootstrap-server kafka:9092 \
		--partitions 1 --replication-factor 1

# Produce 200 random messages to Kafka topic
seed:
	docker compose exec -T kafka sh -lc '\
		echo "Producing 200 msgs..."; \
		for i in $$(seq 1 200); do \
		printf "{\"user_id\":\"u%s\",\"event\":\"click\",\"value\":%s,\"ts\":%s}\n" \
	"$$((RANDOM%5))" "$$((RANDOM%100))" "$$(date +%s%3N)"; \
	sleep 0.05; \
	done | /opt/bitnami/kafka/bin/kafka-console-producer.sh --bootstrap-server kafka:9092 --topic events.raw'


# Flink SQL: Kafka -> Iceberg (HadoopCatalog on MinIO)
flink-sql:
	docker compose exec -T flink-jobmanager \
	./bin/sql-client.sh \
	-i /opt/flink/sql/job_statements/01_set_s3a.sql \
	-f /opt/flink/sql/job_statements/02_create_catalog.sql \
	-f /opt/flink/sql/job_statements/03_use_catalog.sql \
	-f /opt/flink/sql/job_statements/04_create_db.sql \
	-f /opt/flink/sql/job_statements/05_use_db.sql \
	-f /opt/flink/sql/job_statements/06_create_table.sql \
	-f /opt/flink/sql/job_statements/07_insert.sql


# Run Spark job to read from Kafka and write to Parquet
spark-job:
	docker compose exec -T spark-master spark-submit \
		--master spark://spark-master:7077 \
		--conf spark.hadoop.fs.s3a.endpoint=$$S3_ENDPOINT \
		--conf spark.hadoop.fs.s3a.path.style.access=true \
		--conf spark.hadoop.fs.s3a.access.key=$$AWS_ACCESS_KEY_ID \
		--conf spark.hadoop.fs.s3a.secret.key=$$AWS_SECRET_ACCESS_KEY \
		--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.apache.hadoop:hadoop-aws:3.3.4 \
		/opt/spark/jobs/stream_kafka_to_parquet.py
