#!/usr/bin/env python3
"""Generate minimal project pages for the CrossNetwork GitHub Pages sites."""
import json
import pathlib
import sys

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{name} — CrossNetwork</title>
    <meta name="description" content="{desc}" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <style>
      :root {{
        color-scheme: dark;
        --bg: #101014; --card: #17171d; --line: #2a2a35;
        --text: #e8e8ee; --muted: #9a9aa8; --accent: #ffa600;
      }}
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0; min-height: 100vh; background: var(--bg); color: var(--text);
        font: 15px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        display: flex; flex-direction: column;
      }}
      main {{ width: 100%; max-width: 720px; margin: 0 auto; padding: 64px 20px 40px; flex: 1; }}
      .head {{ display: flex; align-items: center; gap: 12px; margin-bottom: 26px; }}
      .mark {{
        width: 40px; height: 40px; border-radius: 11px; display: grid; place-items: center;
        font-weight: 700; font-size: 11px; letter-spacing: 0.06em; color: #14140f;
        background: linear-gradient(135deg, #ffc766, var(--accent));
      }}
      .org {{ font-size: 12.5px; letter-spacing: 0.09em; text-transform: uppercase; color: var(--muted); }}
      .org a {{ color: var(--muted); text-decoration: none; }}
      h1 {{ margin: 0 0 10px; font-size: 30px; letter-spacing: -0.02em; word-break: break-word; }}
      .desc {{ margin: 0 0 22px; color: #c3c3d0; font-size: 16px; }}
      .chips {{ display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 26px; }}
      .chip {{
        font-size: 12px; color: var(--muted); border: 1px solid var(--line);
        border-radius: 999px; padding: 3px 11px;
      }}
      .actions {{ display: flex; gap: 10px; flex-wrap: wrap; }}
      .btn {{
        display: inline-block; padding: 9px 18px; border-radius: 8px; font-size: 14px;
        text-decoration: none; border: 1px solid var(--line); color: var(--text);
      }}
      .btn:hover {{ border-color: #464656; }}
      .btn.primary {{ background: var(--accent); border-color: var(--accent); color: #17130a; font-weight: 600; }}
      .btn.primary:hover {{ background: #ffb733; }}
      footer {{
        max-width: 720px; width: 100%; margin: 0 auto; padding: 18px 20px 34px;
        border-top: 1px solid var(--line); color: var(--muted); font-size: 12.5px;
        display: flex; gap: 14px; flex-wrap: wrap;
      }}
      footer .copy {{ margin-right: auto; }}
      footer a {{ color: var(--text); text-decoration: underline dotted; }}
    </style>
  </head>
  <body>
    <main>
      <div class="head">
        <span class="mark" aria-hidden="true">CN</span>
        <span class="org"><a href="https://crossnetwork.uk">CrossNetwork</a></span>
      </div>

      <h1>{name}</h1>
      <p class="desc">{desc}</p>

      <div class="chips">
        <span class="chip">{lang}</span>
        <span class="chip">{license}</span>
        <span class="chip">{domain}</span>
      </div>

      <div class="actions">
        <a class="btn primary" href="{repo}">Source</a>
{extra}
      </div>
    </main>

    <footer>
      <span class="copy">© CrossNetwork</span>
      <a href="https://crossnetwork.uk">All projects</a>
      <a href="{repo}/issues">Issues</a>
    </footer>
  </body>
</html>
"""

FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="CrossNetwork">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#ffc766"/>
      <stop offset="1" stop-color="#ffa600"/>
    </linearGradient>
  </defs>
  <rect width="64" height="64" rx="14" fill="url(#g)"/>
  <text x="32" y="44" text-anchor="middle" fill="#14140f"
        font-family="system-ui, -apple-system, 'Segoe UI', Roboto, Arial, sans-serif"
        font-size="26" font-weight="800" letter-spacing="-0.5">CN</text>
</svg>
"""

PROJECTS = [
    {
        "repo_name": "sam",
        "name": "SAM",
        "domain": "sam-repo.crossnetwork.uk",
        "desc": "Addons Manager for Stremio: order, logos and Home visibility for your addon collection.",
        "lang": "JavaScript · Vue",
        "license": "AGPL-3.0",
        "extra": '        <a class="btn" href="https://sam.crossnetwork.uk">Live instance</a>\n',
    },
    {
        "repo_name": "CrossStats",
        "name": "CrossStats",
        "domain": "crossstats-repo.crossnetwork.uk",
        "desc": "System stats in your KDE Plasma panel, plus a rich, paginated tooltip.",
        "lang": "Python · KDE Plasma",
        "license": "GPL-2.0",
        "extra": "",
    },
    {
        "repo_name": "qt-esrgan-upscaler",
        "name": "qt-esrgan-upscaler",
        "domain": "qt-esrgan-upscaler-repo.crossnetwork.uk",
        "desc": "Native KDE/Qt6 desktop front-end for batch image upscaling with Real-ESRGAN (ncnn/Vulkan).",
        "lang": "Python · Qt6",
        "license": "GPL-3.0",
        "extra": "",
    },
    {
        "repo_name": "stremio-web-shell",
        "name": "stremio-web-shell",
        "domain": "stremio-web-shell-repo.crossnetwork.uk",
        "desc": "Stremio web client (v5) in a thin Electron shell for Arch Linux, with a self-managed streaming server.",
        "lang": "JavaScript · Electron",
        "license": "GPL-2.0",
        "extra": "",
    },
]


def main(outdir: str) -> None:
    root = pathlib.Path(outdir)
    for p in PROJECTS:
        d = root / p["repo_name"]
        d.mkdir(parents=True, exist_ok=True)
        html = TEMPLATE.format(
            name=p["name"],
            desc=p["desc"],
            lang=p["lang"],
            license=p["license"],
            domain=p["domain"],
            repo=f"https://github.com/SKBlacksmith/{p['repo_name']}",
            extra=p["extra"],
        )
        (d / "index.html").write_text(html, encoding="utf-8")
        (d / "favicon.svg").write_text(FAVICON, encoding="utf-8")
        (d / "CNAME").write_text(p["domain"] + "\n", encoding="utf-8")
        (d / ".nojekyll").write_text("", encoding="utf-8")
    print(json.dumps({p["repo_name"]: p["domain"] for p in PROJECTS}, indent=2))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "out")
