"""
DAG: legacy_to_airflow_dag
Purpose: Simulates migration of a Windows Task Scheduler job into Airflow
Includes: Retry logic, modular Python tasks, email alert on failure
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from airflow.utils.dates import days_ago
from airflow.utils.trigger_rule import TriggerRule
import logging
import time
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv(dotenv_path='/opt/airflow/docker/.env')

# Email recipient (from .env)
ALERT_EMAIL = os.getenv("ALERT_EMAIL", "fallback_email@example.com")

default_args = {
    'owner': 'bita',
    'retries': 2,
    'retry_delay': 60,  # seconds
}

# Define the DAG
with DAG(
    dag_id='legacy_to_airflow_dag',
    default_args=default_args,
    description='Simulated migration of legacy scheduled job to Airflow',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
    tags=['migration', 'etl', 'demo']
) as dag:

    def download_file():
        logging.info("✅ Step 1: Downloading file (mock)...")
        time.sleep(2)  # simulate delay

    def transform_file():
        logging.info("✅ Step 2: Transforming file (mock)...")
        time.sleep(1)

    def upload_file():
        logging.info("✅ Step 3: Uploading file to S3 (mock)...")
        time.sleep(2)

    # Task 1: Simulate file download
    download = PythonOperator(
        task_id='download_file',
        python_callable=download_file,
    )

    # Task 2: Simulate transformation
    transform = PythonOperator(
        task_id='transform_file',
        python_callable=transform_file,
    )

    # Task 3: Simulate file upload
    upload = PythonOperator(
        task_id='upload_file',
        python_callable=upload_file,
    )

    # Task 4: Notify via email if any task fails
    notify_failure = EmailOperator(
        task_id='send_email_on_failure',
        to=ALERT_EMAIL,
        subject='[Airflow] DAG {{ dag.dag_id }} Failed ❌',
        html_content="""
            <p>One or more tasks in DAG <strong>{{ dag.dag_id }}</strong> have failed.</p>
            <p>Please check the <a href="http://localhost:8080">Airflow UI</a> for details.</p>
        """,
        trigger_rule=TriggerRule.ONE_FAILED,
    )

    # Define task dependencies
    download >> transform >> upload >> notify_failure