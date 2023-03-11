import os
import humanize
import imagehash
from PIL import Image, UnidentifiedImageError


def get_image_data(file_path):
    size_bytes = os.path.getsize(file_path)
    size_human = humanize.naturalsize(size_bytes)
    file_name, file_ext = os.path.splitext(file_path)
    try:
        with Image.open(file_path) as im:
            width, height = im.size
            fmt = im.format
            mod = im.mode
            iash = str(imagehash.phash(im))
            old_ext = file_ext.lower()
            new_ext = '.' + fmt.lower()
            store_path = file_path
            if old_ext != new_ext:
                new_file_path = file_name + new_ext
                os.rename(file_path, new_file_path)
                store_path = new_file_path
            return {'sb': size_bytes, 'sh': size_human, "w": width, 'h': height,
                    'f': fmt, 'ph': iash, 'm': mod, 'n': store_path}
    except UnidentifiedImageError:
        return {'sb': size_bytes, 'sh': size_human, 'e': 'UnidentifiedImageError', 'n': file_path}
