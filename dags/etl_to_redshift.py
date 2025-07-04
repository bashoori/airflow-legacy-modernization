"""
DAG: etl_to_redshift
Purpose: Simulates an ETL pipeline from S3 to Redshift (mocked)
Steps:
- Extract raw CSV (mocked S3)
- Transform using external clean_data() from scripts.transform
- Log simulated load to Redshift
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from scripts.transform import clean_data  # Import reusable transform logic

import pandas as pd
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path='/opt/airflow/docker/.env')

# Paths from .env for optional logging (actual logic in transform.py)
S3_INPUT_PATH = os.getenv("S3_INPUT_PATH", "/opt/airflow/scripts/sample_raw_data.csv")
TRANSFORMED_PATH = os.getenv("S3_TRANSFORMED_PATH", "/opt/airflow/scripts/final_output.csv")
REDSHIFT_TABLE = os.getenv("REDSHIFT_TABLE", "mock_table")

default_args = {
    'owner': 'bita',
    'retries': 1,
    'retry_delay': 60,
}

with DAG(
    dag_id='etl_to_redshift',
    default_args=default_args,
    description='ETL pipeline from mocked S3 to Redshift with clean_data module',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
    tags=['etl', 'redshift', 'aws']
) as dag:

    def extract():
        """
        Simulates downloading a file from S3.
        Here it just reads a CSV from local scripts/ folder.
        """
        logging.info(f"📥 Extracting data from {S3_INPUT_PATH}")
        df = pd.read_csv(S3_INPUT_PATH)
        df.to_csv('/opt/airflow/scripts/cleaned_data.csv', index=False)
        logging.info("✅ Raw file extracted and saved locally")

    def load():
        """
        Simulates loading data to Redshift (mock).
        """
        logging.info(f"📤 Loading cleaned data into Redshift table: {REDSHIFT_TABLE}")
        logging.info(f"📂 Data location: {TRANSFORMED_PATH}")
        logging.info("✅ Load complete (mocked)")

    extract_task = PythonOperator(
        task_id='extract_csv',
        python_callable=extract,
    )

    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=clean_data,  # From scripts/transform.py
    )

    load_task = PythonOperator(
        task_id='load_to_redshift',
        python_callable=load,
    )

    extract_task >> transform_task >> load_task