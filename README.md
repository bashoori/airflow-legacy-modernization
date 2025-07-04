# 🚀 Airflow Legacy Job Modernization & ETL Pipeline

This project demonstrates how to migrate legacy **Windows Task Scheduler** jobs to modern, reliable **Apache Airflow DAGs**, containerized with **Docker**, integrated with **AWS-style ETL logic**, and deployed using **GitHub Codespaces** or local Docker Compose.

It includes secure config with `.env`, modular Python scripts, automated email alerts, and a mock ETL pipeline ready for production scaling.

---

## 🧭 Project Goals

- ✅ Migrate legacy batch jobs to **Apache Airflow DAGs**
- ✅ Build clean, modular **ETL pipelines** (mock S3 → transform → Redshift)
- ✅ Use `.env` for secret management (email, AWS, DB)
- ✅ Set up **EmailOperator** for failure alerts
- ✅ Containerize the entire setup using **Docker Compose**
- ✅ Enable CI/CD DAG validation via **GitHub Actions**
- ✅ Prepare for real-world Data Engineering roles (like Intermediate Airflow Developer)

---

## 🗂 Project Structure
```
.
├── dags/                  # Airflow DAGs (3 total)
│   ├── legacy_to_airflow_dag.py
│   ├── etl_to_redshift.py
│   └── email_alert_test.py
├── scripts/               # Reusable data transformation logic
│   └── transform.py
├── data/                  # Sample input and expected output
│   ├── sample_raw_data.csv
│   └── expected_output.csv
├── docker/                # Docker Compose + .env
│   ├── docker-compose.yaml
│   └── .env
├── .github/workflows/     # CI pipeline
│   └── deploy_airflow.yml
└── README.md
```
---

## 🔁 DAGs Overview

### 1️⃣ `legacy_to_airflow_dag.py`
Simulates a 3-step legacy job:
- Download CSV
- Transform (mock logic)
- Upload to S3 (mock)
- Sends email alert on failure (via `EmailOperator`)

### 2️⃣ `etl_to_redshift.py`
Daily ETL pipeline:
- Extract from local CSV (mock S3)
- Clean data via `scripts/transform.py`
- Load into Redshift (simulated with logging)

### 3️⃣ `email_alert_test.py`
Intentionally fails a task to trigger your SMTP email alert.

---

## 🔐 .env Configuration

Used across all scripts and Docker services. Example values:

```env
# Email Alerts
ALERT_EMAIL=your_email@gmail.com
AIRFLOW__SMTP__SMTP_USER=your_email@gmail.com
AIRFLOW__SMTP__SMTP_PASSWORD=your_password
AIRFLOW__SMTP__SMTP_HOST=smtp.gmail.com
AIRFLOW__SMTP__SMTP_PORT=587

# AWS (Mocked)
S3_BUCKET_NAME=my-bucket-name
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret

🐳 Running Locally with Docker
```
cd docker
docker-compose up --build
```
	•	Access Airflow at: http://localhost:8080
	•	Default credentials: airflow / airflow

🧪 Sample Dataset

sample_raw_data.csv
```
customer_id,full_name,email,signup_date,amount_spent
101,Alice Smith,alice@example.com,2023-11-15,250.75
...
```
Transform logic:
	•	Removes incomplete rows
	•	Adds processed_at timestamp
	•	Saves as final_output.csv

⸻

✅ GitHub Actions CI

On each push, GitHub Actions:
	•	Validates all DAGs for syntax errors using py_compile
	•	Prevents broken DAGs from being merged


📊 Visual Diagram
```
Windows Legacy Job
      |
      v
Apache Airflow DAGs
 (Dockerized)

├── Download Task
├── Transform Task (Pandas)
├── Upload Task (Mock S3)
└── Email Alert on Failure

Additional DAG → ETL to Redshift (Mock)
```

```
                +-----------------------+
                |   Windows Task Job    |
                |  (Simulated Legacy)   |
                +----------+------------+
                           |
                           v
                +----------+-----------+
                |   Apache Airflow     |     (via Docker Compose)
                |    Webserver & DAGs  |
                +----------+-----------+
                           |
      +--------------------+---------------------+
      |                    |                     |
      v                    v                     v
+-------------+    +---------------+     +----------------+
|  Download   | -> |  Transform    | --> |   Upload to    |
|  Task       |    |  Task         |     |     S3 (Mock)  |
+-------------+    +---------------+     +----------------+
   (mock S3)          (clean_data)             (Log only)

      |
      v
  Email Alert on Failure
  via EmailOperator
        |
        v
+--------------------+
|   Email: ALERT_EMAIL   |
+--------------------+


        ⤷ Additional Pipeline:
        ----------------------
                +
                |
                v
        +------------------------+
        | ETL to Redshift DAG    |
        +------------------------+
                |
         +------+-------+
         |              |
         v              v
   Extract CSV      Transform CSV
    (mocked S3)      (dropna, timestamp)
         |              |
         +------+-------+
                |
                v
         +--------------+
         |  Load to      |
         | Redshift (Sim)|
         +--------------+
         ```






🙋 About the Author

Bita Ashoori
📍 Vancouver, Canada
🔗 LinkedIn
🔗 Portfolio

⸻

📜 License

This project is licensed under the MIT License.

⸻
