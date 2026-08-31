import json, os, re, sys
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

SRC = r"C:\Users\User1\Downloads\bazinga_imagenes_generadas_chat\Stock SEO"
OUT = r"C:\Users\User1\Downloads\stock-seo-gallery"

def slug(s):
    s = s.lower().replace("&", "and")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return re.sub(r"-+", "-", s)

def title(s):
    s = s.replace("_", " ").replace("-", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s[:1].upper() + s[1:]

jobs = []
for cat in sorted(os.listdir(SRC)):
    cdir = os.path.join(SRC, cat)
    if not os.path.isdir(cdir):
        continue
    cs = slug(cat)
    os.makedirs(os.path.join(OUT, "images", cs), exist_ok=True)
    os.makedirs(os.path.join(OUT, "thumbs", cs), exist_ok=True)
    for fn in sorted(os.listdir(cdir)):
        if not fn.lower().endswith(".png"):
            continue
        jobs.append((cat, cs, fn, os.path.join(cdir, fn)))

print(f"{len(jobs)} images in {len(set(j[1] for j in jobs))} categories", flush=True)

def work(j):
    cat, cs, fn, src = j
    base = slug(os.path.splitext(fn)[0])
    full = os.path.join(OUT, "images", cs, base + ".webp")
    thumb = os.path.join(OUT, "thumbs", cs, base + ".webp")
    try:
        im = Image.open(src).convert("RGB")
        w, h = im.size
        if not os.path.exists(full):
            f = im.copy()
            if max(f.size) > 1536:
                f.thumbnail((1536, 1536), Image.LANCZOS)
            f.save(full, "WEBP", quality=88, method=5)
        if not os.path.exists(thumb):
            t = im.copy()
            t.thumbnail((520, 520), Image.LANCZOS)
            t.save(thumb, "WEBP", quality=76, method=5)
        return {
            "category": cat, "category_slug": cs,
            "title": title(os.path.splitext(fn)[0]),
            "id": f"{cs}/{base}",
            "file": f"images/{cs}/{base}.webp",
            "thumb": f"thumbs/{cs}/{base}.webp",
            "original": fn,
            "width": w, "height": h,
            "bytes": os.path.getsize(full),
        }
    except Exception as e:
        print("ERR", src, e, flush=True)
        return None

with ThreadPoolExecutor(max_workers=8) as ex:
    recs = [r for r in ex.map(work, jobs) if r]

recs.sort(key=lambda r: (r["category"], r["title"]))
cats = {}
for r in recs:
    cats.setdefault(r["category"], {"name": r["category"], "slug": r["category_slug"], "count": 0})
    cats[r["category"]]["count"] += 1

manifest = {
    "name": "Stock SEO Image Library",
    "purpose": "Royalty-free stock imagery for home & auto service businesses, organized by trade. Intended for flyer, ad and social graphic production.",
    "total_images": len(recs),
    "categories": sorted(cats.values(), key=lambda c: c["name"]),
    "images": recs,
}
with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=1, ensure_ascii=False)

with open(os.path.join(OUT, "manifest.csv"), "w", encoding="utf-8", newline="") as f:
    import csv
    w = csv.DictWriter(f, fieldnames=["id","category","title","file","thumb","width","height","bytes","original"], extrasaction="ignore")
    w.writeheader()
    for r in recs: w.writerow(r)

tot = sum(r["bytes"] for r in recs)
print(f"done: {len(recs)} images, images/ = {tot/1e6:.1f} MB", flush=True)
