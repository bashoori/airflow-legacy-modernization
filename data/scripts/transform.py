"""
transform.py
This script is used within Airflow DAGs to clean customer transaction data.
It removes incomplete rows and adds a timestamp for tracking.
"""

import pandas as pd
import logging
import os
from dotenv import load_dotenv

# Load environment variables (for input/output paths)
load_dotenv(dotenv_path='/opt/airflow/docker/.env')

# Set input and output file paths from .env, with fallback defaults
INPUT_PATH = os.getenv("S3_INPUT_PATH", "/opt/airflow/scripts/sample_raw_data.csv")
OUTPUT_PATH = os.getenv("S3_TRANSFORMED_PATH", "/opt/airflow/scripts/final_output.csv")

def clean_data(input_path=INPUT_PATH, output_path=OUTPUT_PATH):
    """
    Loads raw CSV, drops rows with nulls, adds 'processed_at' timestamp,
    and saves the cleaned result.
    """
    try:
        logging.info(f"📥 Reading file from: {input_path}")
        df = pd.read_csv(input_path)

        # Drop rows with any missing values
        initial_rows = len(df)
        df.dropna(inplace=True)
        cleaned_rows = len(df)
        logging.info(f"🧹 Dropped {initial_rows - cleaned_rows} rows with nulls")

        # Add processing timestamp
        df['processed_at'] = pd.Timestamp.now()
        logging.info("📌 Added 'processed_at' column")

        # Save the cleaned file
        df.to_csv(output_path, index=False)
        logging.info(f"✅ Cleaned file saved to: {output_path}")

    except Exception as e:
        logging.error(f"❌ Data cleaning failed: {e}")
        raise