#!/usr/bin/env python3
"""Build Each-Touch Dev Kits public GitHub Pages storefront & interactive JuiceBox 2D playground."""

from __future__ import annotations

import html
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
CATALOG_PATH = ROOT / "kits-catalog.json"
BASE_URL = "https://each-touch.github.io/dev-kits"


def _esc(s: object) -> str:
    return html.escape(str(s or ""), quote=True)


def main() -> int:
    kits = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / ".nojekyll").touch()

    kit = kits[0]
    itch_url = kit.get("itchUrl") or "https://each-touch.itch.io/"
    hl_html = "".join(f"<li>{_esc(h)}</li>" for h in kit.get("highlights", []))

    ld_json = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": kit["shortTitle"],
            "description": kit["tagline"],
            "brand": {"@type": "Brand", "name": "Each-Touch Dev Kits"},
            "offers": {
                "@type": "Offer",
                "priceCurrency": "USD",
                "price": str(kit["priceUsd"]),
                "availability": "https://schema.org/InStock",
                "url": itch_url,
            },
        },
        ensure_ascii=False,
    )

    hub_html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Each-Touch Dev Kits — Commercial HTML5 Game Dev &amp; Creator Source Kits</title>
  <meta name="description" content="Zero-dependency ES module source kits with TypeScript definitions, unit tests, and live browser sandboxes. Try live playgrounds before buying." />
  <link rel="canonical" href="{BASE_URL}/" />
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%2310b981'/%3E%3Ctext x='16' y='21' text-anchor='middle' font-family='monospace' font-weight='800' font-size='14' fill='%230b0f14'%3EDK%3C/text%3E%3C/svg%3E" />
  <script type="application/ld+json">{ld_json}</script>
  <style>
    :root {{
      --bg: #0b0f14; --surface: #131922; --panel: #19212c; --border: rgba(148,163,184,0.18);
      --text: #f1f5f9; --sec: #b6c4d6; --muted: #8b9bb4; --amber: #f59e0b; --cyan: #38bdf8; --green: #10b981;
      --font: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      --mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }}
    * {{ box-sizing: border-box; }}
    html, body {{ margin: 0; padding: 0; background: var(--bg); color: var(--text); font-family: var(--font); font-size: 14px; line-height: 1.5; overflow-x: hidden; }}
    a {{ color: var(--cyan); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .topbar {{ display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 10px 18px; background: var(--surface); border-bottom: 1px solid var(--border); flex-wrap: wrap; }}
    .brand {{ display: inline-flex; align-items: center; gap: 10px; color: var(--text); font-weight: 800; font-size: 15px; }}
    .mark {{ width: 28px; height: 28px; border-radius: 7px; background: linear-gradient(135deg, #10b981, #059669); color: #0b0f14; display: inline-flex; align-items: center; justify-content: center; font-family: var(--mono); font-weight: 800; font-size: 13px; }}
    .badges {{ display: flex; gap: 8px; flex-wrap: wrap; }}
    .badge {{ padding: 3px 9px; border-radius: 999px; font-size: 11px; font-weight: 700; border: 1px solid var(--border); background: var(--panel); color: var(--sec); white-space: nowrap; }}
    .badge-green {{ background: rgba(16,185,129,0.14); border-color: rgba(16,185,129,0.38); color: var(--green); }}
    .badge-amber {{ background: rgba(245,158,11,0.14); border-color: rgba(245,158,11,0.38); color: var(--amber); }}
    .badge-cyan {{ background: rgba(56,189,248,0.14); border-color: rgba(56,189,248,0.38); color: var(--cyan); }}
    .wrap {{ max-width: 1180px; margin: 0 auto; padding: 18px 18px 28px; }}
    .hero {{ background: radial-gradient(circle at 86% 18%, rgba(16,185,129,0.15), transparent 45%), var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 22px 24px; display: grid; grid-template-columns: 1.4fr 1fr; gap: 20px; align-items: center; }}
    .hero h1 {{ margin: 8px 0 8px; font-size: clamp(22px, 3vw, 32px); line-height: 1.15; }}
    .hero p {{ margin: 0 0 14px; color: var(--sec); font-size: 14.5px; }}
    .btn {{ display: inline-flex; align-items: center; justify-content: center; padding: 9px 15px; border-radius: 7px; font-weight: 700; font-size: 13px; border: 1px solid rgba(148,163,184,0.3); background: var(--panel); color: var(--text); }}
    .btn:hover {{ text-decoration: none; border-color: var(--cyan); }}
    .btn-primary {{ background: var(--amber); border-color: var(--amber); color: #0b0f14; }}
    .hero-stats {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
    .stat {{ background: var(--panel); border: 1px solid var(--border); border-radius: 10px; padding: 11px 13px; }}
    .stat strong {{ display: block; color: var(--green); font-size: 15px; }}
    .stat span {{ font-size: 12px; color: var(--sec); }}
    .section-title {{ margin: 22px 0 10px; font-size: 13px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted); font-weight: 700; }}
    .kit-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 18px; display: flex; flex-direction: column; gap: 10px; }}
    .kit-top {{ display: flex; justify-content: space-between; gap: 8px; flex-wrap: wrap; }}
    .kit-card h2 {{ margin: 2px 0 0; font-size: 20px; }}
    .kit-card p {{ margin: 0; color: var(--sec); }}
    .kit-card ul {{ margin: 0; padding-left: 18px; color: var(--sec); font-size: 13px; }}
    .ecosystem {{ margin-top: 22px; background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 14px 16px; display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; font-size: 12.5px; color: var(--sec); }}
    .eco-links {{ display: flex; gap: 12px; flex-wrap: wrap; }}
    @media (max-width: 820px) {{
      .hero {{ grid-template-columns: 1fr; padding: 16px; }}
      .btn {{ width: 100%; }}
    }}
  </style>
</head>
<body>
  <header class="topbar">
    <a class="brand" href="./"><span class="mark">DK</span><span>Each-Touch Dev Kits</span></a>
    <div class="badges">
      <span class="badge badge-green">Zero Dependencies</span>
      <span class="badge badge-cyan">ES Modules + .d.ts</span>
      <span class="badge badge-amber">Live Sandboxes + Unit Tested</span>
    </div>
  </header>

  <main class="wrap">
    <section class="hero">
      <div>
        <span class="badge badge-green">Commercial Source Kits for Indie Studios</span>
        <h1>Ship Faster with Drop-In, Zero-Dependency HTML5 &amp; JS Kits</h1>
        <p>Every kit comes with tested ES Modules, TypeScript declarations, playable standalone demos, and a commercial project license. Test live in your browser before buying.</p>
        <div style="display:flex; gap:10px; flex-wrap:wrap;">
          <a class="btn btn-primary" href="./juicebox-2d/">Open Live JuiceBox 2D Playground</a>
          <a class="btn" href="{_esc(itch_url)}" target="_blank" rel="noopener noreferrer">Buy Full Kit (${kit['priceUsd']:.2f})</a>
        </div>
      </div>
      <div class="hero-stats">
        <div class="stat"><strong>12 Modules</strong><span>Shake, Hitstop, Springs, Particles</span></div>
        <div class="stat"><strong>Zero Deps</strong><span>Pure ES6 + TypeScript .d.ts</span></div>
        <div class="stat"><strong>Unit Tested</strong><span>100% verified with node --test</span></div>
        <div class="stat"><strong>Free Demo</strong><span>Interactive sandbox + Lite ZIP</span></div>
      </div>
    </section>

    <div class="section-title">Flagship Commercial Kit</div>
    <section class="kit-card">
      <div class="kit-top">
        <span class="badge badge-cyan">{_esc(kit['category'])}</span>
        <span class="badge badge-amber">${kit['priceUsd']:.2f} USD · Free Lite Demo</span>
      </div>
      <h2><a href="./juicebox-2d/" style="color:var(--text);">{_esc(kit['shortTitle'])}</a></h2>
      <p>{_esc(kit['tagline'])}</p>
      <ul>{hl_html}</ul>
      <div style="display:flex; gap:10px; flex-wrap:wrap; padding-top:6px;">
        <a class="btn btn-primary" href="./juicebox-2d/">Launch Interactive Playground</a>
        <a class="btn" href="{_esc(itch_url)}" target="_blank" rel="noopener noreferrer">Buy Commercial Kit (${kit['priceUsd']:.2f})</a>
        <a class="btn" href="./demos/juicebox-2d-free-lite-demo.zip" download>Download Free Lite ZIP</a>
      </div>
    </section>

    <footer class="ecosystem">
      <span>Each-Touch Creative Ecosystem · Commercial Source Kits, Tools &amp; Assets</span>
      <div class="eco-links">
        <a href="https://each-touch.github.io/forge-tools/" target="_blank" rel="noopener noreferrer">Forge Tools</a>
        <a href="https://each-touch.github.io/asset-lab/" target="_blank" rel="noopener noreferrer">Asset Lab</a>
        <a href="https://each-touch.github.io/print-play-lab/" target="_blank" rel="noopener noreferrer">Print-Play Lab</a>
        <a href="https://each-touch.github.io/" target="_blank" rel="noopener noreferrer">Each-Touch Arcade</a>
      </div>
    </footer>
  </main>
</body>
</html>
"""
    (DOCS / "index.html").write_text(hub_html, encoding="utf-8")

    # Also update buy link inside docs/juicebox-2d/index.html if present
    jb_index = DOCS / "juicebox-2d" / "index.html"
    if jb_index.is_file():
        txt = jb_index.read_text(encoding="utf-8")
        txt = txt.replace("__ITCH_BUY_URL__", _esc(itch_url))
        jb_index.write_text(txt, encoding="utf-8")

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    (DOCS / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'  <url>\n    <loc>{BASE_URL}/</loc>\n    <lastmod>{today}</lastmod>\n    <priority>1.0</priority>\n  </url>\n'
        f'  <url>\n    <loc>{BASE_URL}/juicebox-2d/</loc>\n    <lastmod>{today}</lastmod>\n    <priority>0.9</priority>\n  </url>\n</urlset>\n',
        encoding="utf-8",
    )
    (DOCS / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n", encoding="utf-8")
    print(f"Built Dev Kits showcase -> {DOCS / 'index.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
