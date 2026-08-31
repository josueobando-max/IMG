# Deploy this gallery to GitHub Pages

The folder is already a git repo with everything committed (786 files, ~131 MB — well inside
GitHub Pages' 1 GB limit). Three steps.

## 1. Create an empty public repo

Go to <https://github.com/new>, name it `stock-seo` (or anything you like), set it **Public**,
and do **not** add a README, .gitignore or license — the repo must start empty.

## 2. Bake in the public URL and push

Run this from inside `C:\Users\User1\Downloads\stock-seo-gallery`, replacing
`YOUR-USERNAME` (and the repo name if you changed it):

```bash
bash deploy.sh YOUR-USERNAME stock-seo
```

Git will ask you to sign in to GitHub the first time. That step is yours — it needs your
credentials.

## 3. Turn on Pages

In the new repo: **Settings → Pages → Source: Deploy from a branch → Branch: `main` / `/ (root)`
→ Save.** Give it ~1–2 minutes.

Your link is then:

```
https://YOUR-USERNAME.github.io/stock-seo/
```

---

## What you send to the AI

The gallery link, plus one line of context:

> Image library for flyer production: https://YOUR-USERNAME.github.io/stock-seo/
> Machine-readable index: https://YOUR-USERNAME.github.io/stock-seo/manifest.json
> Read AI-README.md at that base for how it is organised. Every image is a direct,
> public, hot-linkable URL — download the `file` URL for the full-resolution 1536×1024 WebP.

That is enough for ChatGPT, Gemini, Claude or any agent with web access to browse the
catalog and pull the exact shots it needs.

## Files an AI will use

| File | What it is |
|---|---|
| `manifest.json` | 389 records: `category`, `title`, `file`, `url`, `width`, `height`, `bytes` |
| `manifest.csv` | Same index, spreadsheet-friendly |
| `urls.txt` | Flat newline-separated list of all 389 full-res URLs |
| `AI-README.md` | Usage brief + category table + flyer-cropping notes |
| `index.html` | Human gallery — search, category filter, copy-URL per image |

## Re-running things

- **Changed the repo/URL?** `python tools/set-base-url.py https://new-base/path` then commit + push.
- **Added new PNGs to the source folder?** `python tools/rebuild-from-png.py` (it skips images
  already converted), then `python tools/set-base-url.py <your base>`, then commit + push.

## Browsing locally without deploying

```bash
python -m http.server 8765 -d "C:/Users/User1/Downloads/stock-seo-gallery"
```

Then open <http://localhost:8765>. Opening `index.html` by double-click also works, but a
server is closer to how the live site behaves.
