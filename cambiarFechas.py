import os
import json
import piexif
import sys
from PIL import Image
from datetime import datetime

def change_file_date_and_exif(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.lower().endswith(('.gif', '.png', '.jpg', '.jpeg', '.tiff', '.mp4', '.avi', '.mov', '.flv')):
                image_file_path = os.path.join(root, file)
                fjson = file.replace('-editado', '')

                json_file_path = os.path.join(root, fjson + '.json')
                try:
                    with open(json_file_path, 'r') as json_file:
                        data = json.load(json_file)
                        if 'photoTakenTime' in data:
                            date_time_original = data['photoTakenTime']['timestamp']
                            date_time_original = datetime.fromtimestamp(int(date_time_original))
                        
                            # We change the date in the EXIF data of the photo.
                            # if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff')):

                            #     image = Image.open(image_file_path)
                            #     exif_dict = piexif.load(image.info['exif'])

                            #     if exif_dict:
                            #         exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = date_time_original.strftime('%Y:%m:%d %H:%M:%S')
                            #         exif_bytes = piexif.dump(exif_dict)
                            #         image.save(image_file_path, exif=exif_bytes)

                            timestamp = date_time_original.timestamp()
                            os.utime(image_file_path, (timestamp, timestamp))
                            os.utime(json_file_path, (timestamp, timestamp))
                        else:
                            print(f"Error processing file {image_file_path}: Date not found")
                except Exception as e:
                    print(f"Error processing file {image_file_path}: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        change_file_date_and_exif(".")
    else:
        directory_path = sys.argv[1]
        change_file_date_and_exif(directory_path)
