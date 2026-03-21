import os
from datetime import datetime
from typing import Optional
import exifread


def _parse_exif_date(val: str) -> Optional[datetime]:
    try:
        # EXIF format: 'YYYY:MM:DD HH:MM:SS'
        return datetime.strptime(str(val), '%Y:%m:%d %H:%M:%S')
    except Exception:
        return None


def get_image_date(path: str) -> Optional[datetime]:
    """Return the best available datetime for an image.

    Try EXIF DateTimeOriginal, then other EXIF tags, then file mtime.
    """
    try:
        with open(path, 'rb') as f:
            tags = exifread.process_file(f, stop_tag='DateTimeOriginal', details=False)
            for key in ('EXIF DateTimeOriginal', 'EXIF DateTimeDigitized', 'Image DateTime'):
                if key in tags:
                    dt = _parse_exif_date(tags[key])
                    if dt:
                        return dt
    except Exception:
        pass

    # fallback to file modified time
    try:
        m = os.path.getmtime(path)
        return datetime.fromtimestamp(m)
    except Exception:
        return None


def sort_images_by_date(paths: list) -> list:
    return sorted(paths, key=lambda p: (get_image_date(p) or datetime.fromtimestamp(0)))
