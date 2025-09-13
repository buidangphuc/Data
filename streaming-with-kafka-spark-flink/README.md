# Kafka + Spark + Flink + MinIO + Iceberg (HadoopCatalog) — All-in-One Lab

Stack via **Docker Compose**:

- **Kafka (KRaft)** + **Schema Registry**
- **Spark 3.5** (Structured Streaming)
- **Flink 1.18** (SQL client) với Kafka + Iceberg + S3 connectors
- **MinIO** (S3-compatible) for **Iceberg** catalog via **HadoopCatalog** (no Hive Metastore)

Jobs:
1. **Flink SQL**: `Kafka -> Iceberg (HadoopCatalog on MinIO)`
2. **Spark Structured Streaming**: `Kafka -> Parquet` (+5s windowed agg)

## Quickstart
```bash
make up
make topics
make seed
make flink-sql
make spark-job


Open UIs:
- **MinIO Console**: http://localhost:9001  (user: `minio`, pass: `minio12345`)
- **Flink UI**:     http://localhost:8081
- **Spark UI**:     Shows in driver logs for the submitted job
- **Schema Registry**: http://localhost:8085

To tear down:
```bash
make down       # stop & keep volumes
make nuke       # stop & remove volumes/images (danger)
```

---

## Data Flow

- Topic: `events.raw` (JSON records with `user_id`, `event`, `value`, `ts` in ms).
- **Flink** reads `events.raw` → writes **Iceberg** table `demo.db/events_iceberg` (in **MinIO** at `s3a://warehouse/iceberg/...`).
- **Spark** reads the same topic → writes **Parquet** to `s3a://warehouse/parquet/events_stream/` and a windowed aggregate to `s3a://warehouse/parquet/agg_5s/`.