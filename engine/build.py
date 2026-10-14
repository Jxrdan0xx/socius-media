"""Render Socius Instagram slides (1080x1350 JPEG) from a JSON spec.

Usage: python3 engine/build.py <spec.json> <out_dir>
Spec: list of posts {"id": str, "slides": [slide, ...]}. One slide = static post.
Slide fields: type (cover|statement|cta), eyebrow, title (wrap highlight words in
<span class='g'>..</span>), sub, chips [str], rows [[title, desc?]], buttons [str].
See engine/example_spec.json.
"""
import base64, json, sys, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
def b64(p): return base64.b64encode((ROOT / p).read_bytes()).decode()
MARK = f"data:image/png;base64,{b64('assets/mark.png')}"
WORD = f"data:image/png;base64,{b64('assets/wordmark.png')}"

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000}
.s{width:1080px;height:1350px;position:relative;overflow:hidden;background:#0C0F22;
  font-family:'Inter',sans-serif;color:#fff;padding:88px 88px 80px;display:flex;flex-direction:column}
.s::before{content:"";position:absolute;inset:0;
  background:radial-gradient(800px 600px at 105% -5%,rgba(162,28,240,.28),transparent 60%),
             radial-gradient(800px 700px at -10% 108%,rgba(20,140,248,.22),transparent 60%);}
.s::after{content:"";position:absolute;inset:0;opacity:.18;
  background-image:radial-gradient(rgba(255,255,255,.55) 1px,transparent 1.2px);background-size:36px 36px;
  -webkit-mask-image:linear-gradient(180deg,transparent 0%,#000 40%,#000 70%,transparent 100%)}
.s>*{position:relative;z-index:2}
.ghost{position:absolute!important;z-index:1!important;opacity:.07;width:900px;right:-260px;bottom:-140px}
.top{display:flex;justify-content:space-between;align-items:center}
.brand{display:flex;align-items:center;gap:18px}
.brand .m{height:52px}.brand .w{height:24px;opacity:.95}
.count{font:500 24px 'Inter';letter-spacing:.12em;color:rgba(255,255,255,.5)}
.body{flex:1;display:flex;flex-direction:column;justify-content:center}
.eyebrow{display:inline-flex;align-self:flex-start;align-items:center;gap:14px;font:600 26px 'Inter';
  letter-spacing:.16em;text-transform:uppercase;color:#B9C3FF;margin-bottom:44px}
.eyebrow::before{content:"";width:44px;height:4px;border-radius:2px;background:linear-gradient(90deg,#A21CF0,#14A0F8)}
h1{font:700 104px/1.04 'Poppins';letter-spacing:-.025em}
h2{font:700 82px/1.08 'Poppins';letter-spacing:-.02em}
.g{background:linear-gradient(100deg,#B03BFF 0%,#6A5CFF 45%,#1BA6FF 100%);-webkit-background-clip:text;background-clip:text;color:transparent}
.sub{font:400 38px/1.45 'Inter';color:rgba(255,255,255,.72);margin-top:44px;max-width:860px}
.chips{display:flex;flex-wrap:wrap;gap:18px;margin-top:56px}
.chip{font:500 32px 'Inter';padding:20px 32px;border-radius:999px;border:2px solid rgba(140,150,255,.35);
  background:rgba(255,255,255,.04)}
.rows{margin-top:56px;display:flex;flex-direction:column;gap:22px}
.row{display:flex;gap:30px;align-items:flex-start;padding:34px 38px;border-radius:28px;
  background:linear-gradient(135deg,rgba(255,255,255,.07),rgba(255,255,255,.02));border:1.5px solid rgba(255,255,255,.1)}
.row .n{font:700 34px 'Poppins';min-width:62px;background:linear-gradient(135deg,#B03BFF,#1BA6FF);
  -webkit-background-clip:text;background-clip:text;color:transparent;line-height:1.35}
.row .t{font:600 36px/1.3 'Poppins'}
.row .d{font:400 29px/1.45 'Inter';color:rgba(255,255,255,.65);margin-top:6px}
.cta{margin-top:60px;display:flex;flex-direction:column;gap:22px;align-items:flex-start}
.btn{font:600 36px 'Poppins';padding:28px 46px;border-radius:999px;
  background:linear-gradient(100deg,#A21CF0,#4F6BFF 55%,#14A0F8);box-shadow:0 18px 50px rgba(90,80,255,.35)}
.btn.o{background:transparent;border:2px solid rgba(255,255,255,.35);box-shadow:none;font-weight:500}
.foot{display:flex;justify-content:space-between;align-items:center;font:500 25px 'Inter';color:rgba(255,255,255,.5)}
.swipe{display:flex;align-items:center;gap:14px;color:rgba(255,255,255,.75)}
.bar{display:flex;gap:8px}.bar i{width:26px;height:6px;border-radius:3px;background:rgba(255,255,255,.18)}
.bar i.on{background:linear-gradient(90deg,#A21CF0,#14A0F8);width:52px}
.bigmark{height:150px;margin-bottom:56px;align-self:flex-start}
"""

def slide(s, i, n):
    t = s["type"]; h = ""
    ghost = f'<img class="ghost" src="{MARK}">' if t in ("cover", "cta") else ""
    if s.get("eyebrow"): h += f'<div class="eyebrow">{s["eyebrow"]}</div>'
    if t == "cta": h = f'<img class="bigmark" src="{MARK}">' + h
    tag = "h1" if t == "cover" else "h2"
    h += f'<{tag}>{s["title"]}</{tag}>'
    if s.get("sub"): h += f'<p class="sub">{s["sub"]}</p>'
    if s.get("chips"): h += '<div class="chips">' + "".join(f'<span class="chip">{c}</span>' for c in s["chips"]) + "</div>"
    if s.get("rows"):
        h += '<div class="rows">' + "".join(
            f'<div class="row"><div class="n">{k+1:02d}</div><div><div class="t">{r[0]}</div>'
            + (f'<div class="d">{r[1]}</div>' if len(r) > 1 else "") + "</div></div>"
            for k, r in enumerate(s["rows"])) + "</div>"
    if s.get("buttons"):
        h += '<div class="cta">' + "".join(
            f'<span class="btn{" o" if k else ""}">{b}</span>' for k, b in enumerate(s["buttons"])) + "</div>"
    bar = ('<div class="bar">' + "".join(f'<i class="{"on" if k == i else ""}"></i>' for k in range(n)) + "</div>") if n > 1 else "<span>sociustalent.com</span>"
    right = '<span class="swipe">Swipe →</span>' if i < n - 1 else "<span>Partners in building the future</span>"
    return f'''<div class="s" id="s{i}">{ghost}
<div class="top"><div class="brand"><img class="m" src="{MARK}"><img class="w" src="{WORD}"></div>
<span class="count">{f"{i+1:02d} / {n:02d}" if n > 1 else ""}</span></div>
<div class="body">{h}</div>
<div class="foot">{bar}{right}</div></div>'''

def render(spec_path, out_dir):
    spec = json.loads(pathlib.Path(spec_path).read_text())
    out = pathlib.Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        for post in spec:
            n = len(post["slides"])
            html = f"<html><head><style>{CSS}</style></head><body>" + "".join(
                slide(s, i, n) for i, s in enumerate(post["slides"])) + "</body></html>"
            pg.set_content(html); pg.wait_for_timeout(300)
            for i in range(n):
                pg.locator(f"#s{i}").screenshot(path=str(out / f'{post["id"]}_{i+1:02d}.jpg'), type="jpeg", quality=90)
            print(post["id"], n)
        b.close()

if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2])
