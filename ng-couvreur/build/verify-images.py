#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contrôle qu'aucune page ne référence une image absente.

Extrait toutes les URLs d'images des pages générées (src, srcset, imagesrcset,
og:image) et vérifie que le fichier correspondant existe. Sort en erreur au
premier manquant : un déploiement avec des images cassées ne doit pas partir.
"""
import os, re, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = os.path.join(ROOT, "site")
BASE = os.environ.get("NG_BASE", "/mediavote-preview/ng-couvreur/site").rstrip("/")
ORIGIN = os.environ.get("NG_SITE_ORIGIN", "").rstrip("/")

IMG_URL = re.compile(r'(?:src|srcset|imagesrcset|content)="([^"]+)"')

def to_path(url):
    url = url.strip()
    if ORIGIN and url.startswith(ORIGIN):
        url = url[len(ORIGIN):]
    if not url.startswith(BASE + "/assets/img/"):
        return None
    return os.path.join(SITE, url[len(BASE) + 1:])

def main():
    pages = glob.glob(os.path.join(SITE, "**", "*.html"), recursive=True)
    refs, missing = set(), []
    for page in pages:
        html = open(page, encoding="utf-8").read()
        for attr in IMG_URL.findall(html):
            for candidate in attr.split(","):
                candidate = candidate.strip().split(" ")[0]
                path = to_path(candidate)
                if not path:
                    continue
                refs.add(path)
                if not os.path.exists(path):
                    missing.append((os.path.relpath(page, SITE), candidate))

    on_disk = len([f for f in os.listdir(os.path.join(SITE, "assets", "img"))
                   if not f.startswith(".")])
    print("%d pages · %d références d'images distinctes · %d fichiers sur le disque"
          % (len(pages), len(refs), on_disk))

    if missing:
        print("\n%d RÉFÉRENCE(S) SANS FICHIER :" % len(missing), file=sys.stderr)
        for page, url in missing[:40]:
            print("  %-46s → %s" % (page, url.split("/")[-1]), file=sys.stderr)
        sys.exit(1)

    unused = on_disk - len(refs)
    print("Toutes les images référencées existent. (%d variantes non utilisées)" % unused)

if __name__ == "__main__":
    main()
