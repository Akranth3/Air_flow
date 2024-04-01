from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def helloworld():
    print("F airflow")

with DAG(dag_id="hello_world",
        start_date=datetime(2024,3,3),
        schedule_interval="@hourly",
        catchup=False) as dag:
        task1 = PythonOperator(task_id="hello_world", python_callable=helloworld)

task1
        
        

