#!/usr/bin/env python3
"""Generates the animated SVGs used by the profile README. Run: python3 build.py"""
import math, random, html
BG, CARD, LINE, LINE2 = "#090e0c", "#111916", "#1f2c27", "#2a3a33"
INK, INK2, INK3, ACC, WARM = "#eef4f0", "#b4c2bb", "#7e8d86", "#5fe3b0", "#f1b76b"
SANS = "'Segoe UI', Inter, system-ui, -apple-system, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
SERIF = "Georgia, 'Times New Roman', serif"
e = html.escape
W = 1200

def shell(h, body, title, extra_style="", extra_defs=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" role="img" aria-label="{e(title)}">
  <title>{e(title)}</title>
  <defs>
    <pattern id="g" width="48" height="48" patternUnits="userSpaceOnUse"><path d="M48 0H0V48" fill="none" stroke="{LINE}" stroke-width="1"/></pattern>
    <radialGradient id="fade" cx="50%" cy="0%" r="90%"><stop offset="0" stop-color="#fff" stop-opacity=".5"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
    <mask id="gm"><rect width="{W}" height="{h}" fill="url(#fade)"/></mask>
    <clipPath id="r"><rect width="{W}" height="{h}" rx="22"/></clipPath>
    <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="60"/></filter>{extra_defs}
  </defs>
  <style>
    .s{{font-family:{SANS}}} .m{{font-family:{MONO}}} .i{{font-family:{SERIF};font-style:italic}}
    @keyframes drift{{to{{transform:translate(60px,30px)}}}} @keyframes tw{{50%{{opacity:.25}}}} @keyframes up{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:none}}}}
    @keyframes blink{{50%{{opacity:0}}}} @keyframes dash{{to{{stroke-dashoffset:0}}}} @keyframes spin{{to{{transform:rotate(360deg)}}}}
    .up{{opacity:0;animation:up .9s cubic-bezier(.22,.8,.22,1) forwards}}
    @media (prefers-reduced-motion:reduce){{*{{animation:none!important}} .up{{opacity:1}}}}{extra_style}
  </style>
  <g clip-path="url(#r)">
    <rect width="{W}" height="{h}" fill="{BG}"/>
    <rect width="{W}" height="{h}" fill="url(#g)" mask="url(#gm)" opacity=".7"/>
    <circle cx="140" cy="-20" r="190" fill="{ACC}" opacity=".16" filter="url(#blur)" style="animation:drift 14s ease-in-out infinite alternate"/>
    <circle cx="{W-120}" cy="{h+10}" r="170" fill="{WARM}" opacity=".09" filter="url(#blur)" style="animation:drift 18s ease-in-out infinite alternate-reverse"/>
{body}
  </g>
  <rect x=".5" y=".5" width="{W-1}" height="{h-1}" rx="22" fill="none" stroke="{LINE2}"/>
</svg>
'''

# ---------- hero ----------
def hero():
    H = 400; cx, cy, R = 925, 200, 138
    g = []
    # rotating meridians: ellipses whose rx sweeps, phase-shifted
    for k in range(6):
        g.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{R}" ry="{R}" fill="none" stroke="{ACC}" stroke-opacity=".28" stroke-width="1"><animate attributeName="rx" values="{R};0;{R}" dur="14s" begin="-{k*14/12:.2f}s" repeatCount="indefinite" calcMode="spline" keySplines=".37 0 .63 1;.37 0 .63 1"/></ellipse>')
    for lat in (-0.72, -0.38, 0, 0.38, 0.72):
        rr = R * math.sqrt(1 - lat * lat)
        g.append(f'<ellipse cx="{cx}" cy="{cy + lat*R:.1f}" rx="{rr:.1f}" ry="{rr*0.16:.1f}" fill="none" stroke="{ACC}" stroke-opacity=".16"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{ACC}" stroke-opacity=".5" stroke-width="1.2"/>')
    random.seed(7)
    pts = []
    for i in range(34):
        a, r = random.random() * 6.283, R * math.sqrt(random.random()) * 0.93
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    for i, (x, y) in enumerate(pts):
        near = sorted(pts, key=lambda p: (p[0]-x)**2 + (p[1]-y)**2)[1]
        g.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{near[0]:.1f}" y2="{near[1]:.1f}" stroke="{ACC}" stroke-opacity=".22"/>')
    for i, (x, y) in enumerate(pts):
        col = WARM if i % 7 == 0 else ACC
        g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{2.6 if i%7==0 else 1.9}" fill="{col}" style="animation:tw {2.4 + i%5*0.5}s ease-in-out -{i*0.37:.2f}s infinite"/>')
    # orbits with travelling signals
    orb = [(R + 34, 46, -24, 9, WARM), (R + 58, 30, 18, 13, ACC), (R + 16, 70, 62, 11, INK)]
    for k, (rx, ry, rot, dur, col) in enumerate(orb):
        d = f"M{cx-rx},{cy} a{rx},{ry} 0 1,0 {2*rx},0 a{rx},{ry} 0 1,0 {-2*rx},0"
        g.append(f'<g transform="rotate({rot} {cx} {cy})"><path id="o{k}" d="{d}" fill="none" stroke="{LINE2}" stroke-dasharray="2 7"/>'
                 f'<circle r="4" fill="{col}"><animateMotion dur="{dur}s" repeatCount="indefinite"><mpath href="#o{k}"/></animateMotion></circle>'
                 f'<circle r="9" fill="{col}" opacity=".18"><animateMotion dur="{dur}s" repeatCount="indefinite"><mpath href="#o{k}"/></animateMotion></circle></g>')
    lines = ["Building AI systems that companies run on.", "RAG pipelines, agents and automation.", "Odoo ERP, from module to warehouse in 3D."]
    T = 4.2; total = T * len(lines); tw = []
    clips = ""
    for i, t in enumerate(lines):
        w = len(t) * 12.1 + 8
        a, b = i * T / total, (i + 1) * T / total
        kt = [0, a, a + (T*0.36)/total, b - (T*0.12)/total, b, 1] if i else [0, (T*0.36)/total, b - (T*0.12)/total, b, 1]
        vals = [0, 0, w, w, 0, 0] if i else [0, w, w, 0, 0]
        if kt[-1] == kt[-2]: kt, vals = kt[:-1], vals[:-1]
        anim = f'<animate attributeName="width" values="{";".join(f"{v:.0f}" for v in vals)}" keyTimes="{";".join(f"{k:.4f}" for k in kt)}" dur="{total}s" repeatCount="indefinite"/>'
        clips += f'<clipPath id="t{i}"><rect x="64" y="236" width="0" height="40">{anim}</rect></clipPath>'
        tw.append(f'<text x="64" y="262" class="m" font-size="20" fill="{INK2}" clip-path="url(#t{i})">{e(t)}</text>')
    chips, x = [], 64
    for i, c in enumerate(["Python", "Rust", "Go", "TypeScript", "Odoo"]):
        w = len(c) * 8.4 + 30
        chips.append(f'<g class="up" style="animation-delay:{0.9 + i*0.12:.2f}s"><rect x="{x}" y="312" width="{w:.0f}" height="32" rx="16" fill="{CARD}" stroke="{LINE2}"/><circle cx="{x+15}" cy="328" r="3" fill="{ACC}"/><text x="{x+25}" y="333" class="m" font-size="13" fill="{INK2}">{c}</text></g>')
        x += w + 10
    body = f'''    <g>{"".join(g)}</g>
    <g class="up" style="animation-delay:.1s"><circle cx="69" cy="92" r="4" fill="{ACC}"><animate attributeName="opacity" values="1;.3;1" dur="2.4s" repeatCount="indefinite"/></circle>
      <text x="84" y="97" class="m" font-size="13" letter-spacing="2.4" fill="{INK3}">ALENÇON, FRANCE · FOUNDER OF NEURVEXIA</text></g>
    <text x="62" y="176" class="s up" style="animation-delay:.25s" font-size="68" font-weight="700" letter-spacing="-2.4" fill="{INK}">Yassine <tspan class="i" font-weight="400" letter-spacing="-1" fill="{ACC}">Naanani</tspan></text>
    <text x="64" y="216" class="s up" style="animation-delay:.4s" font-size="21" fill="{INK2}">AI engineer · Full-stack developer · Odoo</text>
    {"".join(tw)}
    <rect x="64" y="244" width="2" height="22" fill="{ACC}" opacity=".0"/>
    {"".join(chips)}'''
    return shell(H, body, "Yassine Naanani — AI engineer, full-stack developer and founder of Neurvexia, based in Alençon, France", extra_defs=clips)

# ---------- numbers ----------
def numbers():
    H = 150; items = [("17", "", "Open-source projects"), ("27", "", "Certifications"), ("5", "+", "Languages shipped"), ("2", "", "Continents served")]
    cw = W / 4; b = []
    for i, (n, plus, label) in enumerate(items):
        x = i * cw + 56
        if i: b.append(f'<line x1="{i*cw:.0f}" y1="34" x2="{i*cw:.0f}" y2="{H-34}" stroke="{LINE}"/>')
        b.append(f'<g class="up" style="animation-delay:{0.15*i:.2f}s"><text x="{x:.0f}" y="82" class="s" font-size="50" font-weight="700" letter-spacing="-2" fill="{INK}">{n}<tspan fill="{ACC}">{plus}</tspan></text>'
                 f'<text x="{x:.0f}" y="110" class="s" font-size="15" fill="{INK3}">{label}</text>'
                 f'<path d="M{x:.0f} 124h44" stroke="{ACC}" stroke-width="2" stroke-linecap="round" stroke-dasharray="44" stroke-dashoffset="44" style="animation:dash 1.2s cubic-bezier(.22,.8,.22,1) {0.4+0.15*i:.2f}s forwards"/></g>')
    return shell(H, "    " + "".join(b), "17 open-source projects, 27 certifications, 5+ languages shipped, 2 continents served")

# ---------- stack ----------
def stack():
    groups = [("01", "AI and LLM systems", ["RAG", "LLM agents", "LangChain", "PyTorch", "TensorFlow", "Computer vision", "NLP"]),
              ("02", "Languages", ["Python", "Rust", "Go", "TypeScript", "JavaScript", "SQL"]),
              ("03", "Backend and platform", ["FastAPI", "Django", "React", "Docker", "Kubernetes", "CI/CD", "PostgreSQL", "Redis"]),
              ("04", "ERP and automation", ["Odoo 14–19", "Custom modules", "API integrations", "n8n", "Reporting"])]
    pad, gap = 28, 18; cw = (W - pad * 2 - gap) / 2; b = []; ch = 150
    H = pad * 2 + ch * 2 + gap
    k = 0
    for gi, (n, title, items) in enumerate(groups):
        x0 = pad + (gi % 2) * (cw + gap); y0 = pad + (gi // 2) * (ch + gap)
        b.append(f'<g class="up" style="animation-delay:{gi*0.12:.2f}s"><rect x="{x0:.0f}" y="{y0}" width="{cw:.0f}" height="{ch}" rx="16" fill="{CARD}" stroke="{LINE}"/>'
                 f'<text x="{x0+24:.0f}" y="{y0+40}" class="s" font-size="18" font-weight="600" fill="{INK}">{title}</text>'
                 f'<text x="{x0+cw-24:.0f}" y="{y0+38}" class="m" font-size="12" letter-spacing="2" fill="{ACC}" text-anchor="end">{n}</text></g>')
        x, y = x0 + 24, y0 + 62
        for it in items:
            w = len(it) * 8.1 + 26
            if x + w > x0 + cw - 20: x, y = x0 + 24, y + 40
            first = it == items[0]
            b.append(f'<g class="up" style="animation-delay:{0.35 + k*0.045:.2f}s"><rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="30" rx="15" fill="{"#12241d" if first else BG}" stroke="{ACC if first else LINE2}" stroke-opacity="{".5" if first else "1"}"/>'
                     f'<text x="{x+13:.0f}" y="{y+20}" class="m" font-size="13" fill="{ACC if first else INK2}">{e(it)}</text></g>')
            x += w + 8; k += 1
    return shell(H, "    " + "".join(b), "Stack: AI and LLM systems, languages, backend and platform, ERP and automation")

# ---------- footer ----------
def footer():
    H = 96; seg = "l40 0 l10 -22 l14 44 l12 -34 l10 12 l40 0"
    d = "M-20 48 " + " ".join(["l120 0 " + seg] * 6)
    body = f'''    <path d="{d}" fill="none" stroke="{LINE2}" stroke-width="1.5"/>
    <path d="{d}" fill="none" stroke="{ACC}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="220 1400" stroke-dashoffset="1620" style="animation:dash 5s linear infinite"/>
    <rect x="{W/2-164:.0f}" y="28" width="328" height="40" rx="20" fill="{BG}" stroke="{LINE2}"/>
    <circle cx="{W/2-142:.0f}" cy="48" r="4" fill="{ACC}"><animate attributeName="opacity" values="1;.3;1" dur="2.4s" repeatCount="indefinite"/></circle>
    <text x="{W/2+10:.0f}" y="53" class="m" font-size="13" fill="{INK2}" text-anchor="middle">k11e3r.github.io · neurvexia.com</text>'''
    return shell(H, body, "k11e3r.github.io · neurvexia.com")

for name, fn in (("hero", hero), ("numbers", numbers), ("stack", stack), ("footer", footer)):
    open(f"assets/{name}.svg", "w").write(fn()); print("wrote", name)
