import zipfile
import os

def zip_directory(directory, zip_file):
    with zipfile.ZipFile(zip_file, 'w') as zipf:
        for root, _, files in os.walk(directory):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), directory))

# Example usage:
directory_to_zip = "test"
zip_file_name = "test.zip"
zip_directory(directory_to_zip, zip_file_name)

