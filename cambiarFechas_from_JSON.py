import os
import commentjson
import piexif
import sys
from PIL import Image
from datetime import datetime

def change_file_date_and_exif(path, blnChangeExifData = False):
	for root, dirs, files in os.walk(path):
		print(f"Reading dir {root}")
		
		for json_file in files:
			if json_file.lower().endswith(('.json')):
				json_file_path = os.path.join(root, json_file)

				try:
					with open(json_file_path, 'r') as json_file:
						data = commentjson.load(json_file)
						if 'photoTakenTime' in data:
							date_time_original = data['photoTakenTime']['timestamp']
							date_time_original = datetime.fromtimestamp(int(date_time_original))
						
							# Ajustamos la fecha y hora original a la zona horaria UTC-3
							# utc_minus_3 = pytz.timezone('Etc/GMT-3')
							# date_time_original = date_time_original.replace(tzinfo=pytz.UTC)
							# date_time_modified = date_time_original.astimezone(utc_minus_3)
							# date_time_modified = date_time_original + timedelta(hours=3)
	
							# Cambiamos la fecha en los datos EXIF de la foto
							if blnChangeExifData:
								if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff')):

									image = Image.open(image_file_path)
									exif_dict = piexif.load(image.info['exif'])

									if exif_dict:
										exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = date_time_original.strftime('%Y:%m:%d %H:%M:%S')
										exif_bytes = piexif.dump(exif_dict)
										image.save(image_file_path, exif=exif_bytes)

							timestamp = date_time_original.timestamp()

							os.utime(json_file_path, (timestamp, timestamp))
							
							image_file = data['title']
							image_file_path = os.path.join(root, image_file)

							if os.path.exists(image_file_path):
								os.utime(image_file_path, (timestamp, timestamp))
						else:
							print(f"Error processing file {json_file_path}: Date not found")
				except Exception as e:
					print(f"Error processing file {json_file_path}: {str(e)}")

if __name__ == "__main__":
	if len(sys.argv) != 2:
		change_file_date_and_exif(".")
	else:
		directory_path = sys.argv[1]
		change_file_date_and_exif(directory_path)
