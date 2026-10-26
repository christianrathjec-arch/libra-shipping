#!/usr/bin/env python3
"""Regenerate the photographer shots from Rogier's originals at retina sizes.

  python3 build-images.py "/path/to/Stock foto's Libra"

Writes assets/<name>-w1920.jpg (fallback) plus assets/<name>-w{1600,2400,3200}.jpg
for heroes/band and assets/<name>-w1800.jpg for cards, LANCZOS + light unsharp, JPEG q82 progressive.
The band keeps its green tint via a colour matrix fitted to the current tinted file.
AI/stock placeholders (crewing, husbandry, bunkering, repair, voyage, freight, portraits) are untouched.
"""
import pathlib, sys
import numpy as np
from PIL import Image, ImageFilter
SRC = pathlib.Path(sys.argv[1]); OUT = pathlib.Path(__file__).parent / "assets"
HERO_W = (1600, 2400, 3200)
TINT = 0.5   # band: half the original green tint (Christian, 26 Oct: lighter, like the hero wash)
# name: (original, crop box as fractions l,t,r,b, fallback width, extra widths, tinted?)
SHOTS = {
 "hero-home-3":        ("Portstock-21.jpg", (0,0,.72,1),   1920, HERO_W, False),
 "hero-agency-5":      ("Portstock-35.jpg", (0,0,.70,1),   1920, HERO_W, False),
 "hero-chartering-2":  ("Portstock-22.jpg", (0,0,1,1),     1920, HERO_W, False),
 "hero-contact-2":     ("Portstock-9.jpg",  (0,0,1,1),     1920, HERO_W, False),
 "band-maasmond":      ("Portstock-26.jpg", (0,0,1,1),     1920, HERO_W, True),
 "card-handling":      ("Portstock-20.jpg", (320/5146,0,4656/5146,1), 900, (1800,), False),
 "card-time-2":        ("Portstock-34.jpg", (198/2048,0,1848/2048,1), 900, (1800,), False),
 "card-layby-2":       ("Portstock-30.jpg", (84/3906,0,3417/3906,1),  900, (1800,), False),
}

TINT_M = np.array([[ 0.4536, 0.1666, 0.1323], [ 0.6329, 0.8036, 0.5388], [-0.0995, 0.0274, 0.3239], [-0.0688,-0.0231,-0.0476]])  # fitted 26 Oct to the original tinted band
def fit_tint():
    I = np.vstack([np.eye(3), np.zeros((1,3))])
    return I*(1-TINT) + TINT_M*TINT   # TINT=1 reproduces the old look, 0 = untouched photo
def apply_tint(im, M):
    a = np.asarray(im.convert("RGB")).astype(float)/255
    A = np.concatenate([a, np.ones(a.shape[:2]+(1,))], -1)
    return Image.fromarray((np.clip(A@M,0,1)*255).round().astype("uint8"))

def save(im, path, w):
    h = round(w * im.size[1] / im.size[0])
    r = im.resize((w,h), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=0.8, percent=45, threshold=2))
    r.save(path, "JPEG", quality=76 if w>=3000 else 82, optimize=True, progressive=True, subsampling=1)
    return path.stat().st_size//1024

M = fit_tint()
for name,(orig,(l,t,r,b),fw,extra,tint) in SHOTS.items():
    im = Image.open(SRC/orig).convert("RGB"); W,H = im.size
    im = im.crop((round(l*W), round(t*H), round(r*W), round(b*H)))
    if tint: im = apply_tint(im, M)
    sizes = [(fw, OUT/f"{name}-w{fw}.jpg")] + [(w, OUT/f"{name}-w{w}.jpg") for w in extra if w < im.size[0]*1.02]
    print(name, "from", orig, im.size, "->", ", ".join(f"{w}px {save(im,p,min(w,im.size[0]))}KB" for w,p in sizes))
