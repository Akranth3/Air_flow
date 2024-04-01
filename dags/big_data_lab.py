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
    'data_fetch_pipeline_big_data',
    default_args=default_args,
    description='Pipeline for fetching and processing NOAA data',
    schedule_interval=None,
    start_date=days_ago(1),
    tags=['noaa', 'data_fetch'],
)

base_url = "https://www.ncei.noaa.gov/data/local-climatological-data/access/"
year = "1903/"  # Replace this with the desired year

move_here = "/home/akranth/semester_8/CS5830/required_location"

def select_random_files(num_of_files=3):
    # You can modify this function to select the required number of files randomly

    num_of_files = 3
    location = "/home/akranth/airflow/www.ncei.noaa.gov/data/local-climatological-data/access/"+year
    print(os.listdir(location))
    available_files = os.listdir(location)
    files = random.sample(available_files, num_of_files)
    print(files)

    with open('/home/akranth/airflow/dags/file_names.txt', 'w') as f:
        print("opened")
        for line in files:
            f.write(f"{line}\n")
            print(line)
        print("closed")
    return 

def zip_files():
    # Zip the selected files into an archive
    directory = move_here
    with zipfile.ZipFile('/home/akranth/semester_8/CS5830/data_archive.zip', 'w') as zipf:
        for root, _, files in os.walk(directory):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), directory))

def move_archive():
    # Move the archive to the required location
    os.rename('data_archive.zip', 'path_to_required_location/data_archive.zip')

fetch_location_data_task = BashOperator(
    task_id='fetch_location_data',
    bash_command='wget -r -np --accept csv https://www.ncei.noaa.gov/data/local-climatological-data/access/' + year,
    dag=dag,
)

select_random_files_task = PythonOperator(
    task_id='select_random_files',
    python_callable=select_random_files,
    dag=dag,
)

fetch_individual_files_task = BashOperator(
    task_id='fetch_individual_files',
    bash_command='chmod +x /home/akranth/airflow/dags/task_3.sh && /home/akranth/airflow/dags/./task_3.sh'
',
    dag=dag,
)

zip_files_task = PythonOperator(
     task_id='zip_files',
     python_callable=zip_files,
     dag=dag,
 )

move_archive_task = BashOperator(
    task_id='move_archive',
    bash_command='mv data_archive.zip '+move_here,
    dag=dag,
)

fetch_location_data_task >> select_random_files_task >> fetch_individual_files_task >> zip_files_task >> move_archive_task
