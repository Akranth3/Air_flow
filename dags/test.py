import os
import random
num_of_files = 3
year = '1903/'
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
