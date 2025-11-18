import exifread
import datetime
from pathlib import Path
from PIL import Image, ExifTags, ImageOps

#convert gps coords to decimal
def convert_to_degrees(value):
    deg = float(value.values[0])
    min = float(value.values[1])
    sec = float(value.values[2])

    result = deg + (min/60.0) + (sec/3600.0)
    return result

#shrink images for thumbnail
def make_thumbnail(img_path, out_folder = 'thumbs', size = (142,200)):
    out_dir = Path(out_folder)
    out_dir.mkdir(exist_ok = True)
    img = Image.open(img_path)

    #ran into issue where vertical photos are flipped, here is a fix
    try:
        for orient in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orient] == 'Orientation':
                break
        exif = img.getexif()
        
        if exif[orient] == 3:
            img = img.rotate(180, expand = True)
        elif exif[orient] == 6:
            img = img.rotate(270, expand = True)
        elif exif[orient] == 8:
            img = img.rotate(90, expand = True)
    except (AttributeError, KeyError, IndexError):
        pass

    img = ImageOps.expand(img, border = 200, fill = 'white') #add border
    
    img.thumbnail(size, Image.Resampling.LANCZOS)

    out_path = out_dir/Path(img_path).name
    img.save(out_path)
    return str(out_path)

#extract exif matadata
def get_exif_data(path):
    data = {}
    folder = Path(path)

    for img in folder.iterdir():
        if img.suffix.lower() in ['.png','.jpg','.jpeg','.webp']:
            with open(img, 'rb') as file:
                tags = exifread.process_file(file)

            gps_lat = tags.get('GPS GPSLatitude')
            gps_lat_ref = tags.get('GPS GPSLatitudeRef')
            gps_long = tags.get("GPS GPSLongitude")
            gps_long_ref = tags.get("GPS GPSLongitudeRef")

            gps_time = tags.get('EXIF DateTimeOriginal')
            orient = str(tags.get('Image Orientation'))


            if gps_lat and gps_lat_ref and gps_long and gps_long_ref:
                lat = convert_to_degrees(gps_lat)
                long = convert_to_degrees(gps_long)

                if gps_lat_ref.values[0] != 'N':
                    lat = -lat
                if gps_long_ref.values[0] != 'E':
                    long = -long
            else:
                continue
            
            data[img.name] = {
                'location' : [lat,long],
                'time' : str(gps_time),
                'path' : f'{path}/{img.name}',
                'thumb' : make_thumbnail(f'{path}/{img.name}', out_folder = 'static/thumbs', size = (100,100)),
                'orientation' : str(orient),
            }

    sorted_data = sorted(
        data.items(), 
        key=lambda item: datetime.strptime(item[1]['time'], '%Y:%m:%d %H:%M:%S')
        if item[1]['time'] else datetime.max
    )

    return sorted_data
    

#print(get_exif_data('images/'))

#extract exif matadata
def get_exif_data(path):
    with open(path, 'rb') as file:
        tags = exifread.process_file(file)
    
    gps_lat = tags.get('GPS GPSLatitude')
    gps_lat_ref = tags.get('GPS GPSLatitudeRef')
    gps_long = tags.get("GPS GPSLongitude")
    gps_long_ref = tags.get("GPS GPSLongitudeRef")

    if gps_lat and gps_lat_ref and gps_long and gps_long_ref:
        lat = convert_to_degrees(gps_lat)
        long = convert_to_degrees(gps_long)

        if gps_lat_ref.values[0] != 'N':
            lat = -lat
        if gps_long_ref.values[0] != 'E':
            long = -long
    
    return [long, lat]

res = get_exif_data('testimg.jpg')
print(res)
