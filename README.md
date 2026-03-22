Raspberry Pi Photo Slideshow
===========================

Simple project to scan a USB drive for pictures, sort them by date (metadata or file time), and play a fullscreen slideshow on a connected TV.

Quick overview
- Modules:
  - `utils/scanner.py` — find image files on a mount path
  - `utils/metadata.py` — extract EXIF/mtime dates and sort
  - `slideshow/viewer.py` — fullscreen slideshow using `pygame`
  - `main.py` — CLI entrypoint that ties everything together

Requirements
- Python 3.9+
- See `requirements.txt`

Install and run (on Raspberry Pi)
1. Clone the repo on the Pi. 
2. On the Pi, install dependencies:

```bash
python3 -m pip install --upgrade pip
git clone https://github.com/ujal-sa/pi-photo-slideshow.git
cd pi-photo-slideshow
python3 -m pip install -r requirements.txt
```

3. Plug the USB drive into the Pi and note its mount path (examples: `/media/pi/USB_LABEL`, `/media/USB_LABEL`, `/mnt/USB`).

4. Run the slideshow:

```bash
python3 main.py --path /media/pi/"USB DISK" --interval 6
```

If you omit `--path`, the program will try to auto-detect mounted volumes under `/media`, `/mnt`, and `/Volumes`.

Usage notes for non-developers
- Use the `--path` flag with the mount point if auto-detect misses the USB.
- Press `ESC` or `q` to quit the slideshow.

Files of interest: `main.py`, `utils/scanner.py`, `utils/metadata.py`, `slideshow/viewer.py`
