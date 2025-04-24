from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from ml_model.train_model import train_model
from ml_model.predict import run_prediction

default_args = {"owner": "airflow", "start_date": datetime(2024, 1, 1), "retries": 1}

with DAG(
    "ml_pipeline_aqi",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
) as dag:

    task_train = PythonOperator(task_id="train_model", python_callable=train_model)

    task_predict = PythonOperator(task_id="predict_aqi", python_callable=run_prediction)

    task_train >> task_predict
