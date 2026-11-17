# crossnetwork.uk

The account page for CrossNetwork, served by GitHub Pages at <https://crossnetwork.uk>.

Plain static HTML, no build step, no external assets. `index.html` lists the public
projects; `favicon.svg` is the mark. Publishing source: `main`, root. The custom domain
lives in `CNAME`.

## tools/

`tools/project-pages.py` — the generator that produced the per-project landing pages
(`sam-repo`, `crossstats-repo`, `qt-esrgan-upscaler-repo`, `stremio-web-shell-repo`).
Output goes to each repository's `gh-pages` branch; this repo only keeps the script.
