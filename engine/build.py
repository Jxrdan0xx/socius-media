"""Render Socius Instagram slides (1080x1350 JPEG) from a JSON spec.

Usage: python3 engine/build.py <spec.json> <out_dir>

Spec: a list of posts: {"id": str, "theme": str, "slides": [slide, ...]}
One slide = a static post.

THEMES (set per post with "theme"; a slide can override with its own "theme"):
  midnight  navy + purple/blue glow, Poppins. The house default.
  light     warm paper background, navy text, Instrument Serif headlines. Editorial.
  gradient  full brand gradient background, white Space Grotesk type. Announcements, moments.
  terminal  black, JetBrains Mono, command-line feel. Crypto history, tech moments.
  photo     a real photo fills the slide (slide field "bg": path relative to the spec, or URL),
            dark fade at the bottom, text sits low. Needs Jordan's own photos.

SLIDE TYPES ("type"):
  cover      big hook. Fields: eyebrow, title, sub
  statement  Fields: eyebrow, title, sub, chips [str], rows [[title, desc?]]
  quote      testimonial. Fields: eyebrow, quote, name, role (quotes <= 330 chars per slide)
  stat       one huge number. Fields: eyebrow, stat ("18"), unit ("years"), title, sub
  event      conference/date card. Fields: eyebrow, day ("15–17"), month ("NOV 2026"),
             title (event name), place, sub, chips
  question   conversation starter. Fields: eyebrow, title (the question), options [str], sub
  cta        closing slide. Fields: eyebrow, title, sub, buttons [str]

Wrap 1-3 key words in titles with <span class='g'>..</span> for the accent treatment.
See engine/example_spec.json and posts/*/spec.json for examples.
"""
import base64, json, sys, pathlib, mimetypes
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent

def b64(p):
    return base64.b64encode((ROOT / p).read_bytes()).decode()

MARK = f"data:image/png;base64,{b64('assets/mark.png')}"
WORD = f"data:image/png;base64,{b64('assets/wordmark.png')}"

def font_face(family, file, weight, style="normal"):
    return (f"@font-face{{font-family:'{family}';src:url(data:font/woff2;base64,{b64('fonts/' + file)}) "
            f"format('woff2');font-weight:{weight};font-style:{style}}}")

FONTS = "".join([
    font_face("Poppins", "poppins-latin-500-normal.woff2", 500),
    font_face("Poppins", "poppins-latin-600-normal.woff2", 600),
    font_face("Poppins", "poppins-latin-700-normal.woff2", 700),
    font_face("Inter", "inter-latin-400-normal.woff2", 400),
    font_face("Inter", "inter-latin-500-normal.woff2", 500),
    font_face("Inter", "inter-latin-600-normal.woff2", 600),
    font_face("JBMono", "jetbrains-mono-latin-400-normal.woff2", 400),
    font_face("JBMono", "jetbrains-mono-latin-600-normal.woff2", 600),
    font_face("JBMono", "jetbrains-mono-latin-700-normal.woff2", 700),
    font_face("Instrument", "instrument-serif-latin-400-normal.woff2", 400),
    font_face("Instrument", "instrument-serif-latin-400-italic.woff2", 400, "italic"),
    font_face("Grotesk", "space-grotesk-latin-500-normal.woff2", 500),
    font_face("Grotesk", "space-grotesk-latin-700-normal.woff2", 700),
])

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000}
.s{--bg:#0C0F22;--fg:#fff;--mut:rgba(255,255,255,.7);--dim:rgba(255,255,255,.5);--line:rgba(140,150,255,.35);
  --card:linear-gradient(135deg,rgba(255,255,255,.07),rgba(255,255,255,.02));--cardb:rgba(255,255,255,.1);
  --hf:'Poppins';--hw:700;--bf:'Inter';--grad:linear-gradient(100deg,#B03BFF 0%,#6A5CFF 45%,#1BA6FF 100%);
  --eb:#B9C3FF;
  width:1080px;height:1350px;position:relative;overflow:hidden;background:var(--bg);
  font-family:var(--bf),sans-serif;color:var(--fg);padding:88px 88px 80px;display:flex;flex-direction:column}
.s>*{position:relative;z-index:2}
.fx{position:absolute!important;inset:0;z-index:0!important;pointer-events:none}
.ghost{position:absolute!important;z-index:1!important;opacity:.07;width:900px;right:-260px;bottom:-140px}
.top{display:flex;justify-content:space-between;align-items:center}
.brand{display:flex;align-items:center;gap:18px}.brand .m{height:52px}.brand .w{height:24px;opacity:.95}
.count{font:500 24px var(--bf);letter-spacing:.12em;color:var(--dim)}
.body{flex:1;display:flex;flex-direction:column;justify-content:center}
.eyebrow{display:inline-flex;align-self:flex-start;align-items:center;gap:14px;font:600 26px var(--bf);
  letter-spacing:.16em;text-transform:uppercase;color:var(--eb);margin-bottom:44px}
.eyebrow::before{content:"";width:44px;height:4px;border-radius:2px;background:var(--grad)}
h1{font-family:var(--hf);font-weight:var(--hw);font-size:104px;line-height:1.04;letter-spacing:-.025em}
h2{font-family:var(--hf);font-weight:var(--hw);font-size:82px;line-height:1.08;letter-spacing:-.02em}
.g{background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.sub{font:400 38px/1.45 var(--bf);color:var(--mut);margin-top:44px;max-width:860px}
.chips{display:flex;flex-wrap:wrap;gap:18px;margin-top:56px}
.chip{font:500 32px var(--bf);padding:20px 32px;border-radius:999px;border:2px solid var(--line);background:rgba(255,255,255,.04)}
.rows{margin-top:56px;display:flex;flex-direction:column;gap:22px}
.row{display:flex;gap:30px;align-items:flex-start;padding:34px 38px;border-radius:28px;background:var(--card);border:1.5px solid var(--cardb)}
.row .n{font:700 34px var(--hf);min-width:62px;background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent;line-height:1.35}
.row .t{font:600 36px/1.3 'Poppins'}
.row .d{font:400 29px/1.45 var(--bf);color:var(--mut);margin-top:6px}
.cta{margin-top:60px;display:flex;flex-direction:column;gap:22px;align-items:flex-start}
.btn{font:600 36px 'Poppins';padding:28px 46px;border-radius:999px;color:#fff;
  background:linear-gradient(100deg,#A21CF0,#4F6BFF 55%,#14A0F8);box-shadow:0 18px 50px rgba(90,80,255,.35)}
.btn.o{background:transparent;border:2px solid var(--line);box-shadow:none;font-weight:500;color:var(--fg)}
.foot{display:flex;justify-content:space-between;align-items:center;font:500 25px var(--bf);color:var(--dim)}
.swipe{display:flex;align-items:center;gap:14px;color:var(--mut)}
.bar{display:flex;gap:8px}.bar i{width:26px;height:6px;border-radius:3px;background:var(--cardb)}
.bar i.on{background:var(--grad);width:52px}
.bigmark{height:150px;margin-bottom:56px;align-self:flex-start}
/* quote */
.qm{font:700 240px/0.75 'Instrument',serif;height:120px;background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.quote{font:500 50px/1.32 'Poppins';letter-spacing:-.01em;margin-top:20px}
.quote.sm{font-size:42px}.quote.xs{font-size:36px;line-height:1.38}
.who{margin-top:52px;display:flex;align-items:center;gap:22px}
.who .bar2{width:6px;height:84px;border-radius:3px;background:var(--grad)}
.who .nm{font:600 34px 'Poppins'}.who .rl{font:400 28px var(--bf);color:var(--mut);margin-top:4px}
/* stat */
.stat{font-family:var(--hf);font-weight:var(--hw);font-size:340px;line-height:.9;letter-spacing:-.05em;background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.unit{font:600 54px var(--hf);margin:10px 0 30px;color:var(--fg)}
/* event */
.ev{display:flex;gap:44px;align-items:stretch;margin-bottom:56px}
.date{min-width:300px;padding:34px 36px;border-radius:32px;background:var(--grad);color:#fff;display:flex;flex-direction:column;justify-content:center}
.date .d1{font:700 96px/1 'Grotesk';letter-spacing:-.03em}.date .d2{font:600 28px 'Inter';letter-spacing:.18em;margin-top:14px}
.place{font:500 34px var(--bf);color:var(--mut);margin-top:18px;display:flex;align-items:center;gap:12px}
/* question */
.opts{margin-top:56px;display:flex;flex-direction:column;gap:20px}
.opt{display:flex;align-items:center;gap:26px;font:500 38px var(--bf);padding:28px 34px;border-radius:24px;border:2px solid var(--line);background:rgba(255,255,255,.03)}
.opt b{font:700 32px 'Grotesk';width:62px;height:62px;border-radius:50%;display:grid;place-items:center;background:var(--grad);color:#fff;flex:none}

/* ---------- THEMES ---------- */
.t-midnight::before{content:"";position:absolute;inset:0;z-index:0;
  background:radial-gradient(800px 600px at 105% -5%,rgba(162,28,240,.28),transparent 60%),
             radial-gradient(800px 700px at -10% 108%,rgba(20,140,248,.22),transparent 60%)}
.t-midnight::after{content:"";position:absolute;inset:0;z-index:0;opacity:.18;
  background-image:radial-gradient(rgba(255,255,255,.55) 1px,transparent 1.2px);background-size:36px 36px;
  -webkit-mask-image:linear-gradient(180deg,transparent 0%,#000 40%,#000 70%,transparent 100%)}

.t-light{--bg:#F3F0EA;--fg:#0E1126;--mut:#4A4E66;--dim:#8A8DA0;--line:rgba(14,17,38,.22);--eb:#5B3BE0;
  --card:#fff;--cardb:rgba(14,17,38,.08);--hf:'Instrument';--hw:400;
  --grad:linear-gradient(100deg,#8E1CF0 0%,#4F55F5 50%,#0E8CF0 100%)}
.t-light h1{font-size:150px;line-height:.95;letter-spacing:-.02em}.t-light h2{font-size:118px;line-height:.98;letter-spacing:-.015em}
.t-light .g{font-style:italic}
.t-light .brand .w{filter:brightness(0);opacity:.85}
.t-light .ghost{opacity:.1}
.t-light::after{content:"";position:absolute;left:88px;right:88px;top:170px;height:2px;background:rgba(14,17,38,.12);z-index:0}
.t-light .chip{background:#fff}.t-light .opt{background:#fff}
.t-light .stat{font-size:380px;letter-spacing:-.03em}

.t-gradient{--bg:#3A2FE0;--fg:#fff;--mut:rgba(255,255,255,.85);--dim:rgba(255,255,255,.7);--line:rgba(255,255,255,.55);--eb:#fff;
  --card:rgba(255,255,255,.12);--cardb:rgba(255,255,255,.25);--hf:'Grotesk';--hw:700;
  --grad:linear-gradient(90deg,#fff,#fff)}
.t-gradient::before{content:"";position:absolute;inset:0;z-index:0;
  background:radial-gradient(900px 700px at 100% 0%,#B12CF5 0%,transparent 60%),
             radial-gradient(900px 800px at 0% 100%,#0FA0F7 0%,transparent 60%),linear-gradient(150deg,#7B1FE6,#3646F0 60%,#1290F0)}
.t-gradient::after{content:"";position:absolute;inset:0;z-index:0;opacity:.12;
  background-image:linear-gradient(rgba(255,255,255,.6) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.6) 1px,transparent 1px);
  background-size:90px 90px}
.t-gradient .brand .m,.t-gradient .bigmark,.t-gradient .ghost{filter:brightness(0) invert(1)}
.t-gradient .ghost{opacity:.12}
.t-gradient h1{font-size:118px;letter-spacing:-.04em;line-height:.98}.t-gradient h2{font-size:92px;letter-spacing:-.035em}
.t-gradient .g{color:#fff;-webkit-text-fill-color:#fff;background:none;text-decoration:underline;text-decoration-thickness:8px;text-underline-offset:14px;text-decoration-color:rgba(255,255,255,.55)}
.t-gradient .btn{background:#fff;color:#2B2BD8;box-shadow:0 18px 50px rgba(0,0,0,.2)}
.t-gradient .date{background:#fff;color:#2B2BD8}
.t-gradient .opt b,.t-gradient .row .n{background:#fff;color:#3A2FE0;-webkit-text-fill-color:#3A2FE0}
.t-gradient .row .n{background:none;-webkit-text-fill-color:#fff}
.t-gradient .stat{-webkit-text-fill-color:#fff}

.t-terminal{--bg:#06070D;--fg:#E7E9FF;--mut:#9BA3C7;--dim:#5E6688;--line:rgba(124,92,255,.5);--eb:#7CF2C8;
  --card:rgba(124,92,255,.06);--cardb:rgba(124,92,255,.28);--hf:'JBMono';--hw:700;--bf:'JBMono'}
.t-terminal::before{content:"";position:absolute;inset:0;z-index:0;
  background:repeating-linear-gradient(180deg,rgba(255,255,255,.035) 0 2px,transparent 2px 6px),
             radial-gradient(900px 700px at 50% 40%,rgba(98,70,255,.16),transparent 70%)}
.t-terminal h1{font-size:86px;line-height:1.12;letter-spacing:-.03em}.t-terminal h2{font-size:70px;line-height:1.15;letter-spacing:-.03em}
.t-terminal h1::before,.t-terminal h2::before{content:"> ";color:#7CF2C8}
.t-terminal h1::after,.t-terminal h2::after{content:"";display:inline-block;width:.5em;height:.9em;margin-left:.15em;vertical-align:-.08em;background:#7CF2C8}
.t-terminal .eyebrow{letter-spacing:.06em;text-transform:none}.t-terminal .eyebrow::before{content:"//";width:auto;height:auto;background:none;color:var(--dim)}
.t-terminal .sub{font-size:33px;line-height:1.55}
.t-terminal .chip,.t-terminal .opt{border-radius:10px}.t-terminal .row{border-radius:14px}
.t-terminal .date{border-radius:14px}.t-terminal .date .d1{font-family:'JBMono'}
.t-terminal .stat{font-size:300px}

.t-photo{--fg:#fff;--mut:rgba(255,255,255,.85);--dim:rgba(255,255,255,.7);--line:rgba(255,255,255,.5);--eb:#fff;--card:rgba(10,12,30,.55);--cardb:rgba(255,255,255,.2)}
.t-photo .bgimg{position:absolute!important;inset:0;z-index:0!important;background-size:cover;background-position:center}
.t-photo .shade{position:absolute!important;inset:0;z-index:1!important;
  background:linear-gradient(180deg,rgba(8,10,28,.55) 0%,rgba(8,10,28,0) 22%,rgba(8,10,28,0) 40%,rgba(8,10,28,.88) 72%,rgba(8,10,28,.96) 100%)}
.t-photo .body{justify-content:flex-end;padding-bottom:20px}
.t-photo h1{font-size:96px}.t-photo h2{font-size:76px}
"""

def esc_attr(s):
    return s.replace('"', "&quot;")

def bg_url(src, spec_dir):
    if src.startswith("http"):
        return src
    p = (spec_dir / src).resolve()
    mime = mimetypes.guess_type(str(p))[0] or "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"

def slide(s, i, n, theme, spec_dir):
    t = s["type"]; th = s.get("theme", theme); h = ""
    pre = ""
    if th == "photo" and s.get("bg"):
        pre += f'<div class="bgimg" style="background-image:url(\'{bg_url(s["bg"], spec_dir)}\')"></div><div class="shade"></div>'
    if t in ("cover", "cta") and th != "photo":
        pre += f'<img class="ghost" src="{MARK}">'
    if t == "cta":
        h += f'<img class="bigmark" src="{MARK}">'
    if t == "event":
        h += (f'<div class="ev"><div class="date"><div class="d1">{s.get("day", "")}</div>'
              f'<div class="d2">{s.get("month", "")}</div></div></div>')
    if s.get("eyebrow"):
        h += f'<div class="eyebrow">{s["eyebrow"]}</div>'
    if t == "quote":
        q = s["quote"]; size = "" if len(q) < 170 else ("sm" if len(q) < 260 else "xs")
        h += f'<div class="qm">&ldquo;</div><p class="quote {size}">{q}</p>'
        h += (f'<div class="who"><div class="bar2"></div><div><div class="nm">{s["name"]}</div>'
              f'<div class="rl">{s.get("role", "")}</div></div></div>')
    else:
        if t == "stat":
            h += f'<div class="stat">{s["stat"]}</div>'
            if s.get("unit"): h += f'<div class="unit">{s["unit"]}</div>'
        if s.get("title"):
            tag = "h1" if t == "cover" else "h2"
            h += f'<{tag}>{s["title"]}</{tag}>'
        if t == "event" and s.get("place"):
            h += f'<div class="place">📍 {s["place"]}</div>'
    if s.get("sub"): h += f'<p class="sub">{s["sub"]}</p>'
    if s.get("chips"): h += '<div class="chips">' + "".join(f'<span class="chip">{c}</span>' for c in s["chips"]) + "</div>"
    if s.get("options"):
        h += '<div class="opts">' + "".join(f'<div class="opt"><b>{chr(65 + k)}</b>{o}</div>' for k, o in enumerate(s["options"])) + "</div>"
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
    count = f"{i+1:02d} / {n:02d}" if n > 1 else ""
    return f'''<div class="s t-{th}" id="s{i}">{pre}
<div class="top"><div class="brand"><img class="m" src="{MARK}"><img class="w" src="{WORD}"></div>
<span class="count">{count}</span></div>
<div class="body">{h}</div>
<div class="foot">{bar}{right}</div></div>'''

def render(spec_path, out_dir):
    spec_path = pathlib.Path(spec_path)
    spec = json.loads(spec_path.read_text())
    out = pathlib.Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        for post in spec:
            n = len(post["slides"]); theme = post.get("theme", "midnight")
            html = f"<html><head><meta charset='utf-8'><style>{FONTS}{CSS}</style></head><body>" + "".join(
                slide(s, i, n, theme, spec_path.parent) for i, s in enumerate(post["slides"])) + "</body></html>"
            pg.set_content(html); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
            for i in range(n):
                pg.locator(f"#s{i}").screenshot(path=str(out / f'{post["id"]}_{i+1:02d}.jpg'), type="jpeg", quality=90)
            print(post["id"], n, theme)
        b.close()

if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2])
