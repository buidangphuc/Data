# CDC with Debezium - Learning Repository

This repository is for learning and experimenting with Change Data Capture (CDC) using Debezium, Kafka, PostgreSQL, and related tools.

## Tech Stack
- **Kafka**: Distributed event streaming platform
- **Debezium**: CDC platform for streaming database changes
- **PostgreSQL**: Source database for CDC
- **Kafka UI**: Web interface for managing Kafka
- **pgAdmin**: Web interface for managing PostgreSQL
- **Schema Registry**: Manages Avro schemas for Kafka topics
- **Docker Compose**: Orchestrates all services

## Target
- Understand CDC concepts and architecture
- Practice setting up Debezium with Kafka and PostgreSQL
- Experiment with streaming data changes
- Learn how to use Kafka UI and pgAdmin for monitoring

## Quick Start
1. Clone the repository
2. Run `make up` to start all services
3. Access Kafka UI at [http://localhost:8080](http://localhost:8080)
4. Access pgAdmin at [http://localhost:5050](http://localhost:5050)

## Notes
- All configurations are for local development and learning purposes
- See `Makefile` for useful commands
- See `docker-compose.yaml` for service setup
