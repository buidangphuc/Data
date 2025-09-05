from datetime import datetime
from pathlib import Path
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.models.baseoperator import chain

# Path to the dbt project
DBT_PROJECT_DIR = Path("/opt/airflow/dags/jsonplaceholder")

# Create a standard Airflow DAG
with DAG(
    dag_id="dbt_transform",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
) as dag:
    
    # Set environment variables for dbt
    dbt_env = {
        "DBT_PROFILES_DIR": "/opt/airflow/dags/profiles",
        "DBT_PROJECT_DIR": str(DBT_PROJECT_DIR)
    }
    
    # Create dbt tasks
    dbt_debug = BashOperator(
        task_id="dbt_debug",
        bash_command=f"cd {DBT_PROJECT_DIR} && dbt debug",
        env=dbt_env,
    )
    
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {DBT_PROJECT_DIR} && dbt run",
        env=dbt_env,
    )
    
    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {DBT_PROJECT_DIR} && dbt test",
        env=dbt_env,
    )
    
    # Set task dependencies
    chain(dbt_debug, dbt_run, dbt_test)
