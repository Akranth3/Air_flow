from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import os
import random
import zipfile

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'data_fetch_pipeline',
    default_args=default_args,
    description='Pipeline for fetching and processing NOAA data',
    schedule_interval=None,
    start_date=days_ago(1),
    tags=['noaa', 'data_fetch'],
)

base_url = "https://www.ncei.noaa.gov/data/local-climatological-data/access/"
year = "1903/"  # Replace this with the desired year

url = base_url+year


def select_random_files(num_of_files=3):
    # You can modify this function to select the required number of files randomly

    num_of_files = 3
    location = "/home/akranth/airflow/dag/www.ncei.noaa.gov/data/local-climatological-data/access/"+year
    print(os.listdir(location))
    available_files = os.listdir(location)
    files = random.sample(available_files, num_of_files)
    print(files)

    with open('/home/akranth/airflow/dag/file_names.txt', 'w') as f:
        print("opened")
        for line in files:
            f.write(f"{line}\n")
            print(line)
        print("closed")
    return 

def zip_files(file_list):
    # Zip the selected files into an archive
    with zipfile.ZipFile('data_archive.zip', 'w') as zipf:
        for file_name in file_list:
            zipf.write(file_name)

def move_archive():
    # Move the archive to the required location
    os.rename('data_archive.zip', 'path_to_required_location/data_archive.zip')

fetch_location_data_task = BashOperator(
    task_id='fetch_location_data',
    bash_command='wget -r -np -A "*.csv" '+url,
    dag=dag,
)

select_random_files_task = PythonOperator(
    task_id='select_random_files',
    python_callable=select_random_files,
    dag=dag,
)

fetch_individual_files_task = BashOperator(
    task_id='fetch_individual_files',
    bash_command='bash /home/akranth/airflow/dags/task_3.sh',
    dag=dag,
)

# zip_files_task = PythonOperator(
#     task_id='zip_files',
#     python_callable=zip_files,
#     op_kwargs={'file_list': "{{ task_instance.xcom_pull(task_ids='select_random_files') }}"},
#     dag=dag,
# )

# move_archive_task = BashOperator(
#     task_id='move_archive',
#     bash_command='mv data_archive.zip /path/to/required/location/',
#     dag=dag,
# )

fetch_location_data_task >> select_random_files_task >> fetch_individual_files_task #>> zip_files_task >> move_archive_task
