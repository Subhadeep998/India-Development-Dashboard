#!/usr/bin/env python3
"""India Development Dashboard — daily build.

1. World Bank indicators for India (annual)      -> docs/data/dashboard.json
2. IMF real-GDP-growth projections               -> same file
3. Daily news + official PIB releases per tab    -> same file
4. SVG charts and the README front page

Each source is isolated: if one is down, the last good data is kept, so the
dashboard never goes blank. Usage: python scripts/build.py [--offline]
"""
import datetime as dt
import email.utils
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = yaml.safe_load(open(os.path.join(ROOT, "data", "config.yaml"), encoding="utf-8"))
OUT = os.path.join(ROOT, "docs", "data", "dashboard.json")
CHARTS = os.path.join(ROOT, "assets", "charts")
UA = {"User-Agent": "Mozilla/5.0 (compatible; IndiaDashboard/1.0; +https://github.com/Subhadeep998)"}
NOW = dt.datetime.now(dt.timezone.utc)
IST = NOW + dt.timedelta(hours=5, minutes=30)
SITE = "https://subhadeep998.github.io/India-Development-Dashboard/"
# Official government news sources only (no general media):
# DD News and All India Radio are the public broadcasters; MyGov and RBI are official portals.
JUNK = re.compile(r"(?i)^(untitled|all news|news archive|blog ?description|home|latest news|press release)|archive$|^page \\d")
OFFICIAL_SITES = ["ddnews.gov.in", "newsonair.gov.in", "mygov.in", "rbi.org.in"]


def get(url, timeout=40):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
        return r.read()


# ---------- data sources ----------
def world_bank(code):
    url = f"https://api.worldbank.org/v2/country/IND/indicator/{code}?format=json&per_page=80"
    data = json.loads(get(url))
    if not isinstance(data, list) or len(data) < 2 or not data[1]:
        return []
    pts = [(int(r["date"]), r["value"]) for r in data[1] if r.get("value") is not None and str(r.get("date", "")).isdigit()]
    return sorted(pts)[-35:]


def imf_growth():
    data = json.loads(get("https://www.imf.org/external/datamapper/api/v1/NGDP_RPCH/IND"))
    vals = data.get("values", {}).get("NGDP_RPCH", {}).get("IND", {})
    return sorted((int(y), v) for y, v in vals.items() if v is not None and int(y) >= 2015)


def gnews(query, days, limit):
    q = urllib.parse.quote_plus(f"{query} when:{days}d")
    root = ET.fromstring(get(f"https://news.google.com/rss/search?q={q}&hl=en-IN&gl=IN&ceid=IN:en", 30))
    items = []
    for it in root.iter("item"):
        title = (it.findtext("title") or "").strip()
        src = (it.findtext("source") or "").strip()
        if src and title.endswith(" - " + src):
            title = title[: -len(" - " + src)]
        try:
            d = email.utils.parsedate_to_datetime(it.findtext("pubDate"))
            date = d.astimezone(dt.timezone(dt.timedelta(hours=5, minutes=30))).date().isoformat()
        except Exception:
            date = ""
        title = " ".join(title.split())
        if len(title.split()) < 5 or JUNK.search(title):
            continue  # skip index pages, "Untitled", archives and other non-articles
        items.append({"title": title, "link": it.findtext("link") or "", "source": src, "date": date})
    items.sort(key=lambda x: x["date"], reverse=True)
    seen, out = set(), []
    for n in items:
        key = n["title"].lower()[:70]
        if key not in seen:
            seen.add(key)
            out.append(n)
    return out[:limit]


# ---------- SVG charts ----------
BG, CREAM, MUTED, GRID = "#0D0F12", "#F3EFE6", "#A3A9B4", "rgba(243,239,230,0.12)"
SAFFRON, GREEN, TEAL, GOLD, RED = "#FF9933", "#4CC38A", "#00CCBB", "#E6B85C", "#F2463A"
SANS = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"


def fmt(v):
    a = abs(v)
    if a >= 100:
        return f"{v:,.0f}"
    if a >= 10:
        return f"{v:,.1f}"
    return f"{v:,.2f}"


def svg_chart(path, title, unit, pts, color, kind="line", forecast=None):
    w, h, l, r, t, b = 640, 300, 64, 24, 58, 40
    allpts = pts + (forecast or [])
    xs = [p[0] for p in allpts]
    ys = [p[1] for p in allpts]
    x0, x1 = min(xs), max(xs)
    lo, hi = min(min(ys), 0) if kind == "bar" else min(ys), max(ys)
    pad = (hi - lo) * 0.12 or 1
    lo = lo - (pad if kind != "bar" or lo < 0 else 0)
    hi = hi + pad
    X = lambda x: l + (x - x0) / max(1, x1 - x0) * (w - l - r)
    Y = lambda y: t + (hi - y) / (hi - lo) * (h - t - b)
    g = []
    for i in range(5):
        yv = lo + (hi - lo) * i / 4
        yy = Y(yv)
        g.append(f'<line x1="{l}" x2="{w - r}" y1="{yy:.1f}" y2="{yy:.1f}" stroke="{GRID}"/>'
                 f'<text x="{l - 8}" y="{yy + 4:.1f}" text-anchor="end" font-size="11" fill="{MUTED}">{fmt(yv)}</text>')
    step = max(1, (x1 - x0) // 6)
    for x in range(x0, x1 + 1, step):
        g.append(f'<text x="{X(x):.1f}" y="{h - 14}" text-anchor="middle" font-size="11" fill="{MUTED}">{x}</text>')
    marks = []
    if kind == "bar":
        bw = max(3, (w - l - r) / max(1, len(allpts)) * 0.62)
        zero = Y(0)
        for x, y in pts:
            c = color if y >= 0 else RED
            marks.append(f'<rect x="{X(x) - bw / 2:.1f}" y="{min(Y(y), zero):.1f}" width="{bw:.1f}" height="{abs(zero - Y(y)):.1f}" rx="2" fill="{c}"/>')
        for x, y in forecast or []:
            marks.append(f'<rect x="{X(x) - bw / 2:.1f}" y="{min(Y(y), zero):.1f}" width="{bw:.1f}" height="{abs(zero - Y(y)):.1f}" rx="2" fill="none" stroke="{color}" stroke-dasharray="3 2"/>')
        marks.append(f'<line x1="{l}" x2="{w - r}" y1="{zero:.1f}" y2="{zero:.1f}" stroke="{MUTED}" stroke-width="1"/>')
    else:
        d = " ".join(f"{'M' if i == 0 else 'L'}{X(x):.1f},{Y(y):.1f}" for i, (x, y) in enumerate(pts))
        area = d + f" L{X(pts[-1][0]):.1f},{h - b} L{X(pts[0][0]):.1f},{h - b} Z"
        marks.append(f'<path d="{area}" fill="{color}" opacity="0.12"/><path d="{d}" fill="none" stroke="{color}" stroke-width="2.5" stroke-linejoin="round"/>')
    lx, ly = pts[-1]
    if kind != "bar":
        marks.append(f'<circle cx="{X(lx):.1f}" cy="{Y(ly):.1f}" r="4.5" fill="{color}"/>')
    latest = f"{fmt(ly)} {unit} ({lx})"
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{title}: latest {latest}">
<rect width="{w}" height="{h}" rx="14" fill="{BG}"/>
<g font-family="{SANS}">
<text x="20" y="28" font-size="16" font-weight="700" fill="{CREAM}">{title}</text>
<text x="20" y="46" font-size="12" fill="{MUTED}">Latest: <tspan fill="{color}" font-weight="700">{latest}</tspan>{" · dashed = IMF projection" if forecast else ""}</text>
{"".join(g)}{"".join(marks)}
</g></svg>'''
    open(path, "w", encoding="utf-8").write(svg)


# ---------- build ----------
def main():
    offline = "--offline" in sys.argv
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    os.makedirs(CHARTS, exist_ok=True)
    prev = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
    dash = {"tabs": [], "imf": prev.get("imf", []), "updated": prev.get("updated")}

    if not offline:
        try:
            dash["imf"] = imf_growth()
        except Exception as exc:
            print(f"[imf] {exc}", file=sys.stderr)

    prev_tabs = {t["id"]: t for t in prev.get("tabs", [])}
    for tab in CFG["tabs"]:
        old = prev_tabs.get(tab["id"], {})
        old_ind = {i["code"]: i for i in old.get("indicators", [])}
        t = {k: tab[k] for k in ("id", "title", "icon", "blurb")}
        t["policies"] = [{"name": n, "about": a, "url": u} for n, a, u in tab["policies"]]
        t["indicators"] = []
        for code, name, unit, scale, label in tab["indicators"]:
            scale = float(scale)
            pts = old_ind.get(code, {}).get("raw", [])
            if not offline:
                try:
                    fresh = world_bank(code)
                    if fresh:
                        pts = fresh
                    time.sleep(0.4)
                except Exception as exc:
                    print(f"[wb] {code}: {exc}", file=sys.stderr)
            if pts:
                t["indicators"].append({"code": code, "name": name, "unit": label, "scale": scale, "raw": pts,
                                        "series": [[y, round(v / scale, 3)] for y, v in pts]})
        t["news"], t["pib"] = old.get("news", []), old.get("pib", [])
        if not offline:
            fresh = []
            for site in OFFICIAL_SITES:  # official government sources only
                try:
                    fresh += gnews(f"site:{site} ({tab['news']})", 3, 6)
                    time.sleep(1)
                except Exception as exc:
                    print(f"[news] {tab['id']} {site}: {exc}", file=sys.stderr)
            if fresh:
                seen, merged = set(), []
                for n in sorted(fresh, key=lambda x: x["date"], reverse=True):
                    k = n["title"].lower()[:70]
                    if k not in seen:
                        seen.add(k)
                        merged.append(n)
                t["news"] = merged[:12]
            try:
                t["pib"] = gnews(f"site:pib.gov.in ({tab['pib']})", 7, 8) or t["pib"]
                time.sleep(1)
            except Exception as exc:
                print(f"[pib] {tab['id']}: {exc}", file=sys.stderr)
        dash["tabs"].append(t)

    if not offline:
        dash["updated"] = IST.strftime("%d %b %Y, %H:%M IST")
    json.dump(dash, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    charts(dash)
    readme(dash)
    print("Built dashboard:", sum(len(t["indicators"]) for t in dash["tabs"]), "indicators,",
          sum(len(t["news"]) + len(t["pib"]) for t in dash["tabs"]), "news items.")


def ind(dash, code):
    for t in dash["tabs"]:
        for i in t["indicators"]:
            if i["code"] == code:
                return i
    return None


CHART_SPECS = [  # file, code, title, color, kind
    ("gdp", "NY.GDP.MKTP.CD", "GDP (trillion US$)", SAFFRON, "line"),
    ("growth", "NY.GDP.MKTP.KD.ZG", "Real GDP growth (%)", GREEN, "bar"),
    ("gni-per-capita", "NY.GNP.PCAP.CD", "GNI per capita (US$)", TEAL, "line"),
    ("manufacturing", "NV.IND.MANF.ZS", "Manufacturing (% of GDP)", GOLD, "line"),
    ("co2", "EN.GHG.CO2.MT.CE.AR5", "CO₂ emissions (Mt)", RED, "line"),
    ("renewables", "EG.FEC.RNEW.ZS", "Renewable energy (% of final use)", GREEN, "line"),
    ("education", "SE.TER.ENRR", "Higher-education enrolment (% gross)", TEAL, "line"),
    ("cereal-yield", "AG.YLD.CREL.KG", "Cereal yield (kg/ha)", GOLD, "line"),
]


def charts(dash):
    for fname, code, title, color, kind in CHART_SPECS:
        i = ind(dash, code)
        if not i or len(i["series"]) < 3:
            continue
        pts = [tuple(p) for p in i["series"] if p[0] >= 2000]
        fc = None
        if code == "NY.GDP.MKTP.KD.ZG" and dash.get("imf"):
            last = pts[-1][0]
            fc = [tuple(p) for p in dash["imf"] if p[0] > last]
        svg_chart(os.path.join(CHARTS, f"{fname}.svg"), title, "", pts, color, kind, fc)


def esc(s, n=120):
    s = (s or "").replace("|", "\\|").replace("[", "(").replace("]", ")").strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def kpi(dash, code, scale_label, digits=2):
    i = ind(dash, code)
    if not i:
        return "—", ""
    y, v = i["series"][-1]
    return (f"{v:,.{digits}f}{scale_label}", str(y))


def readme(dash):
    tpl = open(os.path.join(ROOT, "data", "README.template.md"), encoding="utf-8").read()
    gdp, gdp_y = kpi(dash, "NY.GDP.MKTP.CD", " tn", 2)
    gr, gr_y = kpi(dash, "NY.GDP.MKTP.KD.ZG", "%", 1)
    gni, gni_y = kpi(dash, "NY.GNP.PCAP.CD", "", 0)
    fc = [p for p in dash.get("imf", []) if p[0] >= IST.year]
    fc_txt = f"{fc[0][1]:.1f}% ({fc[0][0]})" if fc else "—"
    kpis = ("| 💰 GDP | 📈 Real growth | 👤 GNI per capita | 🔮 IMF growth forecast |\n|:--:|:--:|:--:|:--:|\n"
            f"| **US$ {gdp}**<br><sub>{gdp_y}</sub> | **{gr}**<br><sub>{gr_y}</sub> | **US$ {gni}**<br><sub>{gni_y}</sub> | **{fc_txt}**<br><sub>IMF WEO</sub> |")
    blocks = []
    for t in dash["tabs"]:
        lines = [f"### {t['icon']} {t['title']}", "", f"<sub>{t['blurb']}</sub>", ""]
        top = (t["pib"][:2] + t["news"][:3])[:4]
        if top:
            lines += [f"- {n['date']} · [{esc(n['title'])}]({n['link']}) — _{esc(n['source'], 40)}_" for n in top]
        else:
            lines.append("- _News fills on the next run._")
        lines += ["", f"[Open the {t['title']} tab →]({SITE}#{t['id']})", ""]
        blocks.append("\n".join(lines))
    body = (tpl.replace("{{KPIS}}", kpis).replace("{{NEWS}}", "\n".join(blocks))
            .replace("{{UPDATED}}", dash.get("updated") or "—")
            .replace("{{UPDATED_BADGE}}", urllib.parse.quote((dash.get("updated") or "pending").split(",")[0])))
    open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8").write(body)


if __name__ == "__main__":
    main()
