#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NG COUVREUR — fabrique des dérivés web à partir de la banque d'images.

Les originaux (PNG 2K produits sur Higgsfield) ne sont jamais versionnés :
ce script les télécharge, produit les variantes optimisées, et laisse les
sources intactes dans un cache local ignoré par git.

    python3 ng-couvreur/build/optimize-images.py

Sortie : ng-couvreur/site/assets/img/<num>-<nom>-<largeur>.<avif|webp|jpg>
"""
import csv, os, sys, io, urllib.request, concurrent.futures as cf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CACHE = os.path.join(ROOT, ".cache-originaux")
OUTDIR = os.path.join(ROOT, "site", "assets", "img")

from PIL import Image
try:
    import pillow_avif  # noqa: F401  (enregistre l'encodeur AVIF)
    HAS_AVIF = True
except ImportError:
    HAS_AVIF = False

# Échelles de largeurs par rapport de forme, calées sur les tailles réellement
# affichées (× 2 pour les écrans à haute densité).
LADDERS = {
    "16:9": [640, 960, 1280, 1920, 2560],
    "3:2":  [480, 720, 960, 1440, 1920],
    "1:1":  [400, 600, 800, 1200],
    "3:4":  [480, 720, 960, 1200],
}
FALLBACK_W = {"16:9": 1280, "3:2": 960, "1:1": 800, "3:4": 720}

Q_AVIF, Q_WEBP, Q_JPEG = 52, 78, 82
AVIF_SPEED = 6


def fetch(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        return dest
    req = urllib.request.Request(url, headers={"User-Agent": "ng-couvreur-build/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as fh:
        fh.write(r.read())
    return dest


def variants(row):
    num, name, ratio, urlsrc = row["num"], row["nom"], row["ratio"], row["url"]
    if ratio not in LADDERS:
        return num, 0, "rapport inconnu : %s" % ratio
    src = os.path.join(CACHE, "%s-%s.png" % (num, name))
    try:
        fetch(urlsrc, src)
    except Exception as ex:
        return num, 0, "téléchargement impossible : %s" % ex

    made = 0
    with Image.open(src) as im:
        im = im.convert("RGB")
        base_w = im.width
        for w in LADDERS[ratio]:
            if w > base_w:          # on n'agrandit jamais
                continue
            h = round(im.height * w / base_w)
            # LANCZOS conserve le détail des tuiles sans halo de netteté
            rs = im.resize((w, h), Image.LANCZOS)
            stem = os.path.join(OUTDIR, "%s-%s-%d" % (num, name, w))
            rs.save(stem + ".jpg", "JPEG", quality=Q_JPEG,
                    optimize=True, progressive=True, subsampling=0)
            rs.save(stem + ".webp", "WEBP", quality=Q_WEBP, method=6)
            made += 2
            if HAS_AVIF:
                rs.save(stem + ".avif", "AVIF", quality=Q_AVIF, speed=AVIF_SPEED)
                made += 1
    return num, made, None


def main():
    os.makedirs(CACHE, exist_ok=True)
    os.makedirs(OUTDIR, exist_ok=True)
    manifest = os.path.join(ROOT, "docs", "03-manifeste-images.csv")
    rows = [r for r in csv.DictReader(open(manifest, encoding="utf-8")) if r["num"] not in ("00A", "00B")]

    print("Optimisation de %d visuels — AVIF %s, WebP, JPEG"
          % (len(rows), "activé" if HAS_AVIF else "INDISPONIBLE (plugin absent)"))

    errors = []
    total = 0
    with cf.ThreadPoolExecutor(max_workers=4) as pool:
        for num, made, err in pool.map(variants, rows):
            if err:
                errors.append((num, err)); print("  %-4s ÉCHEC  %s" % (num, err))
            else:
                total += made; print("  %-4s %2d fichiers" % (num, made))

    weight = sum(os.path.getsize(os.path.join(OUTDIR, f)) for f in os.listdir(OUTDIR)
                 if not f.startswith("."))
    print("\n%d fichiers générés — %.1f Mo au total" % (total, weight / 1e6))
    if errors:
        print("\n%d visuel(s) en échec :" % len(errors))
        for n, e in errors:
            print("  %s : %s" % (n, e))
        sys.exit(1)
    print("Terminé.")


if __name__ == "__main__":
    main()
