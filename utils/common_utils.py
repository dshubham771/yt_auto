import os
import shutil


def move_file(source_path, destination_path):
    try:
        if os.path.exists(source_path):
            shutil.move(source_path, destination_path)
            print(f"File moved successfully from '{source_path}' to '{destination_path}'")
        else:
            print(f"The file '{source_path}' does not exist.")
    except Exception as e:
        print(f"Error occurred while moving the file from '{source_path}' to '{destination_path}': {e}")