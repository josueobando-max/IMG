#!/usr/bin/env python
"""Export images as JPEG into to-upload/, ready to attach to an AI that cannot browse.

Usage:
  python tools/pick.py <search terms...> [-n COUNT]

Examples:
  python tools/pick.py roofing                  # everything in the Roofing category
  python tools/pick.py plumbing drain -n 5      # 5 plumbing images matching "drain"
  python tools/pick.py "tree services" -n 8
  python tools/pick.py --list                   # show categories and counts
"""
import json, os, re, shutil, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTDIR = os.path.join(ROOT, "to-upload")
m = json.load(open(os.path.join(ROOT, "manifest.json"), encoding="utf-8"))

args = [a for a in sys.argv[1:]]
if "--list" in args or not args:
    print(f"{m['total_images']} images in {len(m['categories'])} categories:\n")
    for c in m["categories"]:
        print(f"  {c['count']:>3}  {c['name']}")
    print("\nusage: python tools/pick.py <search terms...> [-n COUNT]")
    sys.exit(0)

count = 0
if "-n" in args:
    i = args.index("-n")
    count = int(args[i + 1])
    del args[i:i + 2]

terms = [t.lower() for t in args]
hits = [r for r in m["images"]
        if all(t in (r["title"] + " " + r["category"]).lower() for t in terms)]

if not hits:
    print(f"No match for: {' '.join(terms)}\nRun --list to see categories.")
    sys.exit(1)

# spread the picks across distinct concepts rather than taking 4 variants of one shot
def concept(r):
    return re.sub(r"-variant-\d+$", "", r["id"])

if count and count < len(hits):
    seen, spread, leftover = set(), [], []
    for r in hits:
        (spread if concept(r) not in seen else leftover).append(r)
        seen.add(concept(r))
    hits = (spread + leftover)[:count]

if os.path.isdir(OUTDIR):
    shutil.rmtree(OUTDIR)
os.makedirs(OUTDIR)

for n, r in enumerate(hits, 1):
    src = os.path.join(ROOT, r["file"].replace("/", os.sep))
    name = f"{n:02d}-{os.path.basename(r['file']).replace('.webp', '.jpg')}"
    im = Image.open(src).convert("RGB")
    im.save(os.path.join(OUTDIR, name), "JPEG", quality=92, optimize=True,
            progressive=True)
    print(f"  {name}  ({im.size[0]}x{im.size[1]})")

with open(os.path.join(OUTDIR, "_captions.txt"), "w", encoding="utf-8") as f:
    for n, r in enumerate(hits, 1):
        f.write(f"{n:02d}  [{r['category']}]  {r['title']}\n")

mb = sum(os.path.getsize(os.path.join(OUTDIR, f))
         for f in os.listdir(OUTDIR)) / 1e6
print(f"\n{len(hits)} JPEG(s) -> {OUTDIR}  ({mb:.1f} MB)")
print("Drag that folder's contents into the AI chat. _captions.txt lists what each one is.")
