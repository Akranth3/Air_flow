#!/bin/bash

# Source directory
source_dir="/home/akranth/airflow/www.ncei.noaa.gov/data/local-climatological-data/access/1903/"

# Destination directory
destination_dir="/home/akranth/semester_8/CS5830/task_1/"

# File containing filenames
filename_list="/home/akranth/airflow/dags/file_names.txt"

# Check if source directory exists
if [ ! -d "$source_dir" ]; then
    echo "Source directory '$source_dir' not found."
    exit 1
fi

# Check if destination directory exists, if not create it
if [ ! -d "$destination_dir" ]; then
    mkdir -p "$destination_dir"
fi

# Check if filename list exists
if [ ! -f "$filename_list" ]; then
    echo "File containing filenames '$filename_list' not found."
    exit 1
fi

# Loop through each filename in the list
while IFS= read -r filename; do
    # Check if file exists in source directory
    if [ -f "$source_dir/$filename" ]; then
        # Move file to destination directory
        mv "$source_dir/$filename" "$destination_dir/"
        echo "Moved '$filename' to '$destination_dir'"
    else
        echo "File '$filename' not found in '$source_dir'."
    fi
done < "$filename_list"
