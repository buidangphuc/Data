#!/usr/bin/env bash
set -euo pipefail
kafka-topics.sh --create --topic events.raw --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1 || true
