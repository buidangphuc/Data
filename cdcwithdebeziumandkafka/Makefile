.PHONY: up down reset logs ui topics create produce consume pg-init connector status delete

up:
	docker compose up -d

down:
	docker compose down

reset:
	docker compose down -v
	docker compose up -d

logs:
	docker compose logs -f

ui:
	@echo "Kafka UI: http://localhost:8080"
	@echo "pgAdmin: http://localhost:5050"

topics:
	docker compose exec kafka kafka-topics --bootstrap-server kafka:9092 --list

create:
	docker compose exec kafka kafka-topics --bootstrap-server kafka:9092 --create --if-not-exists --topic demo --partitions 1 --replication-factor 1

produce:
	docker compose exec kafka kafka-console-producer --bootstrap-server kafka:9092 --topic demo

consume:
	docker compose exec kafka kafka-console-consumer --bootstrap-server kafka:9092 --topic demo --from-beginning

pg-init:
	docker compose exec -T postgres psql -U admin -d pyblog -c "CREATE TABLE IF NOT EXISTS public.posts (id SERIAL PRIMARY KEY, title TEXT, body TEXT, created_at TIMESTAMPTZ DEFAULT now());"
	docker compose exec -T postgres psql -U admin -d pyblog -c "INSERT INTO public.posts (title, body) VALUES ('hello','from debezium');"

connector:
			curl -X PUT http://localhost:8083/connectors/pg-source/config \
				-H "Content-Type: application/json" \
				-d @connector-config.json

status:
	curl -s http://localhost:8083/connectors/pg-source/status | jq .

delete:
	curl -s -X DELETE http://localhost:8083/connectors/pg-source
