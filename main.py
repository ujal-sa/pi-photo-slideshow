#!/usr/bin/env python3
import argparse
import os
import sys
from typing import List

from utils.scanner import find_images
from utils.metadata import sort_images_by_date
from slideshow.viewer import Slideshow


def guess_mounts() -> List[str]:
    roots = ['/media', '/mnt', '/Volumes']
    found = []
    for r in roots:
        if not os.path.exists(r):
            continue
        for child in os.listdir(r):
            p = os.path.join(r, child)
            if os.path.isdir(p):
                found.append(p)
    return found


def choose_mount(auto_paths: List[str]) -> str:
    if not auto_paths:
        return ''
    if len(auto_paths) == 1:
        return auto_paths[0]
    print('Multiple mount points found:')
    for i, p in enumerate(auto_paths, 1):
        print(f'{i}) {p}')
    try:
        sel = int(input('Choose number (or 0 to cancel): '))
        if sel <= 0 or sel > len(auto_paths):
            return ''
        return auto_paths[sel - 1]
    except Exception:
        return ''


def main():
    parser = argparse.ArgumentParser(description='USB Photo Slideshow')
    parser.add_argument('--path', help='Mount path to scan for images')
    parser.add_argument('--interval', type=float, default=5.0, help='Seconds per image')
    args = parser.parse_args()

    mount = args.path
    if not mount:
        candidates = guess_mounts()
        mount = choose_mount(candidates)

    if not mount:
        print('No mount path provided or selected. Exiting.')
        sys.exit(1)

    images = find_images(mount)
    images = sort_images_by_date(images)

    if not images:
        print('No images found under', mount)
        sys.exit(1)

    viewer = Slideshow(images, interval=args.interval)
    viewer.run()


if __name__ == '__main__':
    main()
