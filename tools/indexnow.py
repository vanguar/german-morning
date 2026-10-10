#!/usr/bin/env python3
"""Tell IndexNow search engines (Bing, Yandex, Seznam, Naver …) about every page in sitemap.xml.

Run after GitHub Pages has published the new build (≈1 minute after `git push`):

    python tools/indexnow.py            # submit all sitemap URLs
    python tools/indexnow.py --dry-run  # only list them

The key file <KEY>.txt lies in the site root, so the key covers /german-morning/.
Google does not use IndexNow: for Google submit sitemap.xml in Search Console.
"""
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://vanguar.github.io/german-morning/"
KEY = next(p.stem for p in ROOT.glob("*.txt") if re.fullmatch(r"[0-9a-f]{32}", p.stem))


def main():
    urls = re.findall(r"<loc>([^<]+)</loc>", (ROOT / "sitemap.xml").read_text(encoding="utf-8"))
    print(f"{len(urls)} URL, key {KEY}")
    if "--dry-run" in sys.argv:
        print("\n".join(urls))
        return
    body = json.dumps({"host": "vanguar.github.io", "key": KEY, "keyLocation": f"{BASE}{KEY}.txt",
                       "urlList": urls}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print("IndexNow:", r.status, "(200/202 = принято)")
    except urllib.error.HTTPError as e:
        print("IndexNow:", e.code, e.read().decode(errors="replace")[:300])
        sys.exit(1)


if __name__ == "__main__":
    main()
