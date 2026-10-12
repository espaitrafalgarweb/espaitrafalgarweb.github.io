#!/usr/bin/env python3
"""Genera les variants AVIF, WebP i JPEG de les quatre imatges del lloc.

Les imatges originals no es versionen: son a source-assets/, que ve del lliurament
del client. Aquest script escriu a public/img/, que si que es versiona.

Cal Pillow amb suport AVIF i WebP. S'executa des de l'arrel del projecte:

    python3 tools/build-images.py
"""

import pathlib
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "source-assets"
OUT = ROOT / "public" / "img"

# name, source file, crop aspect ratio, widths to emit
JOBS = [
    ("facana", SRC / "Fotos-Trafalgar/003.jpg", 3 / 2, [640, 960, 1280, 1920]),
    ("obres", SRC / "obres-master.jpg", 3 / 2, [640, 960, 1280, 1920]),
    ("render-sala", SRC / "Renders-Trafalgar/Copia-de-IMATGE-2-B.jpg", 4 / 3, [400, 800]),
    ("render-treball", SRC / "Renders-Trafalgar/Copia-de-IMATGE-1-B.jpg", 4 / 3, [400, 800]),
]


def crop_to(im, ratio):
    w, h = im.size
    if w / h > ratio:
        new_w = int(h * ratio)
        box = ((w - new_w) // 2, 0, (w - new_w) // 2 + new_w, h)
    else:
        new_h = int(w / ratio)
        box = (0, (h - new_h) // 2, w, (h - new_h) // 2 + new_h)
    return im.crop(box)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, path, ratio, widths in JOBS:
        base = Image.open(path).convert("RGB")
        base = crop_to(base, ratio)
        for width in widths:
            height = round(width / ratio)
            im = base.resize((width, height), Image.LANCZOS)
            im.save(OUT / f"{name}-{width}.jpg", quality=82, optimize=True, progressive=True)
            im.save(OUT / f"{name}-{width}.webp", quality=78, method=6)
            im.save(OUT / f"{name}-{width}.avif", quality=58)
            print(f"{name}-{width}: {width}x{height}")

    # Imatge per a Open Graph, 1200x630, a partir de la foto de la façana.
    og = crop_to(Image.open(SRC / "Fotos-Trafalgar/003.jpg").convert("RGB"), 1200 / 630)
    og.resize((1200, 630), Image.LANCZOS).save(
        OUT / "og-espai-trafalgar.jpg", quality=84, optimize=True, progressive=True
    )
    print("og-espai-trafalgar: 1200x630")


if __name__ == "__main__":
    main()
