import json, os, html, sys

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = (sys.argv[1] if len(sys.argv) > 1 else "").rstrip("/")

m = json.load(open(os.path.join(OUT, "manifest.json"), encoding="utf-8"))
imgs, cats = m["images"], m["categories"]


def abs_url(p):
    return f"{BASE}/{p}" if BASE else p


# ---------- machine-readable outputs ----------
if BASE:
    m["base_url"] = BASE
    m["manifest_url"] = f"{BASE}/manifest.json"
    for r in imgs:
        r["url"] = abs_url(r["file"])
        r["thumb_url"] = abs_url(r["thumb"])
else:
    # no base given: drop any absolute URLs a previous run baked in
    m.pop("base_url", None)
    m.pop("manifest_url", None)
    for r in imgs:
        r.pop("url", None)
        r.pop("thumb_url", None)

json.dump(m, open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)

with open(os.path.join(OUT, "urls.txt"), "w", encoding="utf-8") as f:
    for r in imgs:
        f.write(abs_url(r["file"]) + "\n")

# ---------- AI instructions ----------
cat_lines = "\n".join(f"| {c['name']} | `{c['slug']}` | {c['count']} |" for c in cats)
sample = json.dumps(imgs[0], indent=2, ensure_ascii=False)
readme = f"""# Stock SEO Image Library - for AI agents

{m['total_images']} royalty-free stock images across {len(cats)} home & auto service trades,
sized 1536x1024 WebP. Intended for building flyers, ads and social graphics.

## How to use this library

1. Fetch the machine-readable index: **`{abs_url('manifest.json')}`**
2. Filter `images[]` by `category` (or `category_slug`) and read `title` to pick a fitting shot.
3. Download the image directly from its `file` path (or the `url` field when present).
   Every image is a direct, public, hot-linkable URL - no auth, no redirect.
4. A flat newline-separated list of every image URL is at **`{abs_url('urls.txt')}`**.
   A spreadsheet-friendly index is at **`{abs_url('manifest.csv')}`**.

### manifest.json image record

```json
{sample}
```

## Categories

| Category | Slug | Images |
|---|---|---|
{cat_lines}

## Notes for flyer production

- All images are 3:2 landscape (1536x1024). Crop to 4:5 or 9:16 from the centre-weighted
  subject; most shots keep the subject centred with usable negative space on one side.
- Filenames are descriptive of the scene - use `title` as the caption/alt hint.
- `*-variant-1..4` files are alternative takes of the same concept; pick one per layout so a
  multi-panel flyer does not repeat a near-identical frame.
- No text or logos are burned into these images, so headline overlay is safe anywhere.
"""
open(os.path.join(OUT, "AI-README.md"), "w", encoding="utf-8").write(readme)
open(os.path.join(OUT, "README.md"), "w", encoding="utf-8").write(readme)


# ---------- gallery page ----------
def card(r):
    t = html.escape(r["title"])
    q = html.escape((r["title"] + " " + r["category"]).lower())
    return (
        f'<figure class="card" data-cat="{r["category_slug"]}" data-q="{q}">'
        f'<a class="ph" href="{r["file"]}" target="_blank" rel="noopener">'
        f'<img src="{r["thumb"]}" alt="{t}" loading="lazy" width="520" height="347"></a>'
        f'<figcaption><span class="t">{t}</span>'
        f'<span class="meta"><span class="cat">{html.escape(r["category"])}</span>'
        f'<button class="cp" data-u="{r["file"]}" type="button">Copy URL</button>'
        f'</span></figcaption></figure>'
    )


chips = "\n".join(
    f'<button class="chip" data-cat="{c["slug"]}" type="button">'
    f'{html.escape(c["name"])} <b>{c["count"]}</b></button>' for c in cats)
cards = "\n".join(card(r) for r in imgs)
base_note = (f'<code id="baseurl">{BASE}</code>' if BASE
             else '<code id="baseurl">(set on deploy)</code>')

CSS = """
*{box-sizing:border-box}
:root{--bg:#fbfaf8;--panel:#fff;--ink:#16150f;--dim:#6d6a5f;--line:#e4e0d6;
 --accent:#1d5c4a;--accent-soft:#e8f1ee;--chip:#f2efe8;--code:#f4f1ea}
@media(prefers-color-scheme:dark){:root{--bg:#12120f;--panel:#1a1a16;--ink:#f0eee7;
 --dim:#9b978a;--line:#2c2c25;--accent:#5fbfa0;--accent-soft:#172b25;--chip:#232320;--code:#1f1f1a}}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);
 font:400 15px/1.55 "Segoe UI",system-ui,-apple-system,sans-serif}
a{color:var(--accent)}
.wrap{max-width:1400px;margin:0 auto;padding:0 clamp(14px,3vw,32px)}
header{border-bottom:1px solid var(--line);background:var(--panel)}
.hd{padding:30px 0 24px}
h1{margin:0 0 6px;font-size:clamp(24px,3.4vw,34px);font-weight:700;letter-spacing:-.02em}
.sub{margin:0;color:var(--dim);max-width:62ch}
.stats{display:flex;flex-wrap:wrap;gap:10px 26px;margin:18px 0 0;padding:0;list-style:none;
 font-size:13px;color:var(--dim)}
.stats b{color:var(--ink);font-weight:700}
.ai{margin:22px 0 0;background:var(--accent-soft);border:1px solid var(--line);
 border-radius:10px;padding:16px 18px}
.ai h2{margin:0 0 8px;font-size:13px;font-weight:700;letter-spacing:.08em;
 text-transform:uppercase;color:var(--accent)}
.ai p{margin:0 0 8px;font-size:14px}
.ai ol{margin:0;padding-left:20px;font-size:14px}
.ai li{margin:3px 0}
code{background:var(--code);border:1px solid var(--line);border-radius:5px;padding:1px 6px;
 font:13px/1.4 ui-monospace,Consolas,monospace;word-break:break-all}
.ctl{position:sticky;top:0;z-index:5;background:var(--panel);
 border-bottom:1px solid var(--line);padding:12px 0}
.ctlrow{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
#q{flex:1 1 240px;min-width:180px;padding:9px 12px;font-size:15px;color:var(--ink);
 background:var(--bg);border:1px solid var(--line);border-radius:8px}
#q:focus{outline:2px solid var(--accent);outline-offset:-1px}
.chips{display:flex;gap:7px;overflow-x:auto;padding:10px 0 2px;scrollbar-width:thin}
.chip{flex:0 0 auto;padding:6px 12px;font:inherit;font-size:13px;color:var(--ink);
 background:var(--chip);border:1px solid transparent;border-radius:999px;cursor:pointer;
 white-space:nowrap}
.chip b{color:var(--dim);font-weight:600;margin-left:3px}
.chip[aria-pressed=true]{background:var(--accent);border-color:var(--accent);color:#fff}
.chip[aria-pressed=true] b{color:rgba(255,255,255,.75)}
#count{font-size:13px;color:var(--dim);white-space:nowrap}
.grid{display:grid;gap:16px;padding:24px 0 60px;
 grid-template-columns:repeat(auto-fill,minmax(240px,1fr))}
.card{margin:0;background:var(--panel);border:1px solid var(--line);border-radius:10px;
 overflow:hidden;display:flex;flex-direction:column}
.card.hide{display:none}
.ph{display:block;aspect-ratio:3/2;background:var(--chip)}
.ph img{width:100%;height:100%;object-fit:cover;display:block}
figcaption{padding:9px 11px 10px;display:flex;flex-direction:column;gap:7px;flex:1}
.t{font-size:13px;line-height:1.35;font-weight:600}
.meta{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-top:auto}
.cat{font-size:11px;color:var(--dim);text-transform:uppercase;letter-spacing:.05em}
.cp{font:inherit;font-size:12px;padding:3px 9px;color:var(--accent);background:none;
 border:1px solid var(--line);border-radius:6px;cursor:pointer;white-space:nowrap}
.cp:hover{background:var(--accent-soft)}
.cp.ok{background:var(--accent);border-color:var(--accent);color:#fff}
.empty{padding:60px 0;text-align:center;color:var(--dim)}
.empty.hide{display:none}
"""

JS = r"""
(function(){
 var cards=[].slice.call(document.querySelectorAll('.card')),
     q=document.getElementById('q'), cnt=document.getElementById('count'),
     none=document.getElementById('none'), cat='';
 function apply(){
  var s=q.value.trim().toLowerCase(), terms=s?s.split(/\s+/):[], n=0;
  cards.forEach(function(c){
   var ok=(!cat||c.dataset.cat===cat)&&terms.every(function(t){return c.dataset.q.indexOf(t)>-1});
   c.classList.toggle('hide',!ok); if(ok)n++;
  });
  cnt.textContent=n+' shown'; none.classList.toggle('hide',n>0);
 }
 q.addEventListener('input',apply);
 document.querySelectorAll('.chip').forEach(function(b){
  b.addEventListener('click',function(){
   cat=b.dataset.cat;
   document.querySelectorAll('.chip').forEach(function(x){
    x.setAttribute('aria-pressed',String(x===b))});
   apply();
  });
 });
 document.getElementById('grid').addEventListener('click',function(e){
  var b=e.target.closest('.cp'); if(!b)return;
  var u=new URL(b.dataset.u,location.href).href;
  if(navigator.clipboard)navigator.clipboard.writeText(u);
  var o=b.textContent; b.textContent='Copied'; b.classList.add('ok');
  setTimeout(function(){b.textContent=o;b.classList.remove('ok')},1100);
 });
 var bu=document.getElementById('baseurl');
 if(bu&&bu.textContent.charAt(0)==='(')
  bu.textContent=location.href.replace(/[^/]*$/,'').replace(/\/$/,'');
 apply();
})();
"""

page = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Stock SEO Image Library</title>
<meta name="description" content="{m['total_images']} royalty-free service-trade stock images for flyer and ad production. Direct download URLs, machine-readable manifest.">
<style>{CSS}</style>
</head><body>

<header><div class="wrap hd">
<h1>Stock SEO Image Library</h1>
<p class="sub">{m['total_images']} royalty-free stock photographs across {len(cats)} home &amp;
auto service trades, ready for flyer, ad and social graphic production.</p>
<ul class="stats">
<li><b>{m['total_images']}</b> images</li>
<li><b>{len(cats)}</b> categories</li>
<li><b>1536&times;1024</b> WebP</li>
<li>no text or logos burned in</li>
</ul>

<div class="ai">
<h2>For AI agents / automation</h2>
<p>Every image below is a direct, public, hot-linkable URL. Base: {base_note}</p>
<ol>
<li>Fetch the machine-readable index: <code>manifest.json</code> &mdash; an array of
 <code>images[]</code> with <code>category</code>, <code>title</code>, <code>file</code>,
 <code>width</code>, <code>height</code>.</li>
<li>Filter by <code>category</code> and read <code>title</code> to pick the right shot.</li>
<li>Download the image straight from its <code>file</code> URL &mdash; no auth, no redirect.</li>
<li>Flat URL list: <code>urls.txt</code> &middot; spreadsheet: <code>manifest.csv</code>
 &middot; full brief: <code>AI-README.md</code></li>
</ol>
</div>
</div></header>

<div class="ctl"><div class="wrap">
<div class="ctlrow">
<input id="q" type="search" placeholder="Search {m['total_images']} images &mdash; roofing, drain, ceramic coating..." autocomplete="off">
<span id="count"></span>
</div>
<div class="chips">
<button class="chip" data-cat="" aria-pressed="true" type="button">All <b>{m['total_images']}</b></button>
{chips}
</div>
</div></div>

<main class="wrap">
<div class="grid" id="grid">
{cards}
</div>
<p class="empty hide" id="none">No images match that search.</p>
</main>

<script>{JS}</script>
</body></html>"""

open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(page)
open(os.path.join(OUT, ".nojekyll"), "w").write("")
print("index.html", len(page) // 1024, "KB | base =", BASE or "(relative)")
