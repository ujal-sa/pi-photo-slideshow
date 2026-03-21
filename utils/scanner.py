import os
from typing import List

IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}


def is_image_file(path: str) -> bool:
    _, ext = os.path.splitext(path.lower())
    return ext in IMAGE_EXTS


def find_images(root: str) -> List[str]:
    """Recursively find image files under `root`.

    Returns a list of absolute file paths.
    """
    images = []
    if not os.path.isdir(root):
        return images
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            path = os.path.join(dirpath, fn)
            if is_image_file(path):
                images.append(os.path.abspath(path))
    return images
