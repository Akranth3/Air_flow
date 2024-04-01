from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.sensors.file_sensor import FileSensor
import zipfile
import pandas as pd
import geopandas as gpd
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 10),
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
}

dag = DAG(
    'data_visualization_pipeline',
    default_args=default_args,
    description='A DAG to process data and generate visualizations',
    schedule_interval='*/1 * * * *',  # Trigger every 1 minute
)

move_here = "/home/akranth/semester_8/CS5830/required_location"
final_location = "/home/akranth/semester_8/CS5830/data_visualizations"

def unzip_file(file_path, unzip_dir):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(unzip_dir)

def process_csv(csv_file):
    #read the file and extract the relevant columns to process further.
    df = pd.read_csv(csv_file)
    filtered_df = df.iloc[:,[1,2,3,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]]  # Adjust fields as needed
    
    #Adjust the date into monthly format
    filtered_df.iloc[:, 0] = filtered_df.iloc[:, 0].str[5:7]
    return filtered_df.groupby(['LATITUDE', 'LONGITUDE']).agg(list)

def compute_monthly_averages(df):
    
    monthly_averages = df.groupby(pd.Grouper(freq='M')).mean()
    return monthly_averages

def generate_visualization(df):
    # Example visualization, replace with your actual visualization logic
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['Lon'], df['Lat']))
    gdf.plot(column='Windspeed', cmap='coolwarm', legend=True)
    # Export plot to PNG
    plt.savefig('visualization.png')

def delete_file(file_path):
    os.remove(file_path)

file_sensor_task = FileSensor(
    task_id='wait_for_archive',
    poke_interval=5,
    timeout=5,
    filepath=move_here,
    dag=dag,
)

unzip_task = BashOperator(
    task_id='unzip_archive',
    bash_command='unzip '+move_here +' -d ' + final_location,
    dag=dag,
)

process_csv_task = PythonOperator(
    task_id='process_csv',
    python_callable=process_csv,
    op_args=['/path/to/unzipped/data.csv'],
    dag=dag,
)

compute_averages_task = PythonOperator(
    task_id='compute_averages',
    python_callable=compute_monthly_averages,
    provide_context=True,
    dag=dag,
)

generate_visualization_task = PythonOperator(
    task_id='generate_visualization',
    python_callable=generate_visualization,
    provide_context=True,
    dag=dag,
)

delete_file_task = PythonOperator(
    task_id='delete_file',
    python_callable=delete_file,
    op_args=['/path/to/unzipped/data.csv'],
    dag=dag,
)

file_sensor_task >> unzip_task >> process_csv_task >> compute_averages_task >> generate_visualization_task >> delete_file_task

