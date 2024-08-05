import os
import json
import sys
from datetime import datetime

def fix_datetime(path=os.getcwd()):
    extensions = ['gif', 'png', 'jpg', 'jpeg', 'tiff', 'mp4', 'avi', 'mov', 'flv']

    files = []
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            if any(filename.lower().endswith(ext) for ext in extensions):
                files.append(os.path.join(root, filename))

    for file in files:
        file_path, file_name = os.path.split(file)
        file_name_without_ext, extension = os.path.splitext(file_name)

        if file_name_without_ext.endswith(')'):
            index = file_name_without_ext[-3:]
            if index == '(0)':
                index = ''
        else:
            index = ''

        json_file = file_name_without_ext.replace(index, '').replace('-editado', '')
        json_file_path = os.path.join(file_path, f"{json_file}.{extension}{index}"[:46] + '.json')

        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as f:
                json_data = json.load(f)

            if 'photoTakenTime' in json_data and 'timestamp' in json_data['photoTakenTime']:
                new_time = int(json_data['photoTakenTime']['timestamp'])
                try:
                    os.utime(file, (new_time, new_time))
                except OSError:
                    print(f"Failed to update modified time for {file}.")
        else:
            print(f'File not found: {json_file_path}')
            continue

if __name__ == "__main__":
    if len(sys.argv) == 1:
        fix_datetime()
    else:
        fix_datetime(sys.argv[1])