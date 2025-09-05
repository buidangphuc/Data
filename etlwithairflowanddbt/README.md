
# ETL with Airflow and dbt

This directory contains an example of implementing an ETL/ELT pipeline using Apache Airflow and dbt.

## Directory Structure

- `dags/`: Contains Airflow DAGs, e.g., `dbt_transform.py`, `elt_jsonplaceholder.py`.
- `config/`: Configuration for Airflow (`airflow.cfg`).
- `logs/`: DAG run logs.
- `plugins/`: Airflow plugins directory.
- `requirements.txt`: List of required Python packages for Airflow and dbt.
- `docker-compose.yaml`: Start Airflow, dbt, and related services using Docker Compose.
- `Makefile`: Some utility commands.

## Usage Guide

### 1. Start the Environment

```sh
cd etlwithairflowanddbt
cp config/airflow.cfg .  # if needed
# Start the services
docker-compose up -d
```

### 2. Access Airflow UI
- Open your browser and go to: http://localhost:8080
- Log in with the default account (if any):
  - Username: `airflow`
  - Password: `airflow`

### 3. Run a DAG
- In the Airflow UI, enable the `dbt_transform` or `elt_jsonplaceholder` DAG to test the pipeline.
- Monitor logs in the Airflow UI or in the `logs/` directory.

### 4. Configure dbt
- dbt configuration files are located in `dags/jsonplaceholder/`.
- You can run dbt manually inside the container or on your local machine:
  ```sh
  cd dags/jsonplaceholder
  dbt run
  dbt test
  ```
