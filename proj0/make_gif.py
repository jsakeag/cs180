"""
Build the dolly zoom animated GIF from the still photos in images/part3/stills/.

Usage:
    python make_gif.py

Drop your dolly zoom stills into images/part3/stills/ named so they sort in
capture order (e.g. 01.jpg, 02.jpg, ... 08.jpg), then run this script. It will
resize/crop every still to a common size and write images/part3/dolly_zoom.gif.
"""

import glob
import os

from PIL import Image, ImageOps

STILLS_DIR = os.path.join("images", "part3", "stills")
OUTPUT_PATH = os.path.join("images", "part3", "dolly_zoom.gif")

TARGET_SIZE = (720, 720)
FRAME_DURATION_MS = 300
PING_PONG = True


def load_frames():
    paths = sorted(
        glob.glob(os.path.join(STILLS_DIR, "*.jpg"))
        + glob.glob(os.path.join(STILLS_DIR, "*.jpeg"))
        + glob.glob(os.path.join(STILLS_DIR, "*.png"))
        + glob.glob(os.path.join(STILLS_DIR, "*.HEIC"))
    )
    if not paths:
        raise SystemExit(
            f"No stills found in {STILLS_DIR}/. Add your dolly zoom photos there first."
        )

    frames = []
    for path in paths:
        img = Image.open(path)
        img = ImageOps.exif_transpose(img)
        img = img.convert("RGB")
        img = ImageOps.fit(img, TARGET_SIZE, Image.LANCZOS)
        frames.append(img)
        print(f"loaded {path} -> {img.size}")
    return frames


def main():
    frames = load_frames()

    if PING_PONG:
        frames = frames + frames[-2:0:-1]

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    frames[0].save(
        OUTPUT_PATH,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_DURATION_MS,
        loop=0,
    )
    print(f"\nWrote {OUTPUT_PATH} ({len(frames)} frames)")


if __name__ == "__main__":
    main()
