import io, json, datetime as dt, os
import requests, boto3, psycopg2
from psycopg2.extras import execute_values
from airflow.decorators import dag, task
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

# Config
MINIO_ENDPOINT = os.environ.get("MINIO_ENDPOINT", "http://minio:9000")
MINIO_USER = os.environ.get("MINIO_ROOT_USER", "minio")
MINIO_PASS = os.environ.get("MINIO_ROOT_PASSWORD", "minio12345")
S3_BUCKET = os.environ.get("S3_BUCKET", "elt-raw")
S3_PREFIX = os.environ.get("S3_PREFIX", "jsonplaceholder/posts")
API_URL = "https://jsonplaceholder.typicode.com/posts"

PG_CONN = {
    "host": os.environ.get("PG_HOST", "warehouse-pg"),
    "port": int(os.environ.get("PG_PORT", 5432)),
    "dbname": os.environ.get("PG_DB", "analytics"),
    "user": os.environ.get("PG_USER", "analytics"),
    "password": os.environ.get("PG_PASSWORD", "analytics"),
}

def s3_client():
    return boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_USER,
        aws_secret_access_key=MINIO_PASS,
    )

def pg_conn():
    return psycopg2.connect(**PG_CONN)


@dag(dag_id="elt_jsonplaceholder", start_date=dt.datetime(2025,1,1), schedule=None, catchup=False)
def elt_jsonplaceholder():
    extract_task_id = "extract_to_s3"
    dbt_task_id = "dbt_transform"
    load_task_id = "load_to_postgres"

    def extract_to_s3_callable(**context):
        resp = requests.get(API_URL, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        buf = io.BytesIO()
        for rec in data:
            buf.write((json.dumps(rec) + "\n").encode())
        buf.seek(0)
        key = f"{S3_PREFIX}/date={dt.date.today().isoformat()}/posts.ndjson"
        s3_client().put_object(Bucket=S3_BUCKET, Key=key, Body=buf)
        context['ti'].xcom_push(key='s3_key', value=key)
        context['ti'].xcom_push(key='count', value=len(data))

    def load_to_postgres_callable(**context):
        key = context['ti'].xcom_pull(task_ids=extract_task_id, key='s3_key')
        obj = s3_client().get_object(Bucket=S3_BUCKET, Key=key)
        lines = obj["Body"].read().decode().splitlines()
        rows = [json.loads(line) for line in lines]
        tuples = [(r["id"], r["userId"], r["title"], r["body"], dt.datetime.now()) for r in rows]

        insert_sql = """
            INSERT INTO raw_jsonplaceholder_posts (id, user_id, title, body, ingested_at)
            VALUES %s;
        """
        conn = pg_conn()
        with conn.cursor() as cur:
            execute_values(cur, insert_sql, tuples, page_size=1000)
        conn.commit()

    extract = PythonOperator(
        task_id=extract_task_id,
        python_callable=extract_to_s3_callable,
    )

    dbt_transform = TriggerDagRunOperator(
        task_id=dbt_task_id,
        trigger_dag_id="dbt_transform",
        wait_for_completion=True,
        reset_dag_run=True,
    )

    load = PythonOperator(
        task_id=load_task_id,
        python_callable=load_to_postgres_callable,
    )

    extract >> dbt_transform >> load

elt_jsonplaceholder()
