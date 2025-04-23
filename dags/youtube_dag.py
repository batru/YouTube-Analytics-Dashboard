from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "Batru",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),  
    "email": ["batrudin10@gmail.com"],
    "email_on_failure": True,
    "start_date": datetime(2025, 4, 23)
}

with DAG(
    dag_id="youtube_dag",
    description="This is a DAG that automates the ETL process of YouTube analytics",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False
) as my_dag:

    task_youtube = BashOperator(
        task_id="task_youtube",
        bash_command="source /mnt/c/Users/batru/Downloads/Work/LUX-DE/De_projects/Youtube_Analytics_Pipeline/venv/bin/activate && python3 /mnt/c/Users/batru/Downloads/Work/LUX-DE/De_projects/Youtube_Analytics_Pipeline/controller.py"
    )
