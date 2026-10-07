# German Morning — landing page

Static SEO landing page for **German Morning** 🇩🇪 — a Telegram bot and interactive
German course (A1–B2): [@GermanMorningBot](https://t.me/GermanMorningBot).

- Production: https://vanguar.github.io/german-morning/
  - Ukrainian (default): https://vanguar.github.io/german-morning/uk/
  - Russian: https://vanguar.github.io/german-morning/ru/
  - German: https://vanguar.github.io/german-morning/de/
- Hosting: GitHub Pages, deployed from the `main` branch (root folder).
- Stack: plain HTML + CSS + a few lines of vanilla JS, light and dark theme.
  No trackers, no cookies.

All internal links are relative so the site works under the `/german-morning/`
base path (`404.html` uses `/german-morning/...` because it is served at any path).

Local preview:

```sh
python -m http.server 8080
# open http://localhost:8080/
```

Pages are generated from one template so the uk / ru / de versions stay in sync:

```sh
python tools/build.py   # rewrites index.html, uk/, ru/, de/
```
