"""
DAG: email_alert_test
Purpose: Simulate a task failure and trigger an email alert
Loads ALERT_EMAIL from secure .env file
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from airflow.utils.dates import days_ago
from airflow.utils.trigger_rule import TriggerRule
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(dotenv_path='/opt/airflow/docker/.env')
ALERT_EMAIL = os.getenv("ALERT_EMAIL", "fallback_email@example.com")

def fail_this_task():
    raise ValueError("🚨 This is a test failure for email alert.")

default_args = {
    'owner': 'bita',
    'email_on_failure': False,  # We'll use EmailOperator instead
    'retries': 0,
}

with DAG(
    dag_id='email_alert_test',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    tags=['alert', 'test'],
    description='DAG to simulate failure and test email alert via EmailOperator'
) as dag:

    # This task will fail
    fail_task = PythonOperator(
        task_id='fail_task',
        python_callable=fail_this_task
    )

    # This task sends an email if the above fails
    alert_task = EmailOperator(
        task_id='send_alert_email',
        to=ALERT_EMAIL,
        subject='[ALERT] Airflow task failed: {{ dag.dag_id }}',
        html_content="""
            <h3>🚨 Task Failure Detected</h3>
            <p>Task <strong>{{ task_instance.task_id }}</strong> in DAG <strong>{{ dag.dag_id }}</strong> has failed.</p>
            <p>Check the <a href="http://localhost:8080">Airflow UI</a> for details.</p>
        """,
        trigger_rule=TriggerRule.ONE_FAILED
    )

    fail_task >> alert_task