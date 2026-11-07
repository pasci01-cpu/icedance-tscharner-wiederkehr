#!/usr/bin/env python3
"""Builds one page per couple from template.html + teams.json, and data/results.js from data/results.json.
Run after editing any of: template.html, teams.json, <dir>/data/results.json.  Usage: python3 build.py"""
import json, os, html, re
ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
teams = json.load(open("teams.json", encoding="utf-8"))
tpl = open("template.html", encoding="utf-8").read()
# cache-busting version: changes whenever app/styles/data change
import hashlib
h = hashlib.sha1()
for f in ["app.js", "styles.css", "template.html", "teams.json"] + [os.path.join(t["dir"], "data/results.json") for t in teams]:
    if os.path.exists(f): h.update(open(f, "rb").read())
v = h.hexdigest()[:8]
for t in teams:
    d = t["dir"]
    root = "" if d == "." else "../" * len(d.split("/"))
    links = []
    for o in teams:
        href = root + ("" if o["dir"] == "." else o["dir"] + "/")
        cur = ' aria-current="page"' if o is t else ""
        links.append('<a href="%s"%s>%s</a>' % (href or "./", cur, html.escape(o["short"])))
    nav = '<nav class="teams" aria-label="Couples">%s</nav>' % "".join(links) if len(teams) > 1 else ""
    vals = {**{k: html.escape(str(x)) for k, x in t.items()}, "root": root, "v": v, "nav": nav}
    page = re.sub(r"\{\{(\w+)\}\}", lambda m: vals[m.group(1)], tpl)
    os.makedirs(os.path.join(d, "data"), exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page)
    src = os.path.join(d, "data/results.json")
    if os.path.exists(src):
        data = open(src, encoding="utf-8").read()
        json.loads(data)  # validate
        open(os.path.join(d, "data/results.js"), "w", encoding="utf-8").write("window.SKATE_DATA = " + data.strip() + ";\n")
    print(f"built {d}/index.html" + ("" if os.path.exists(src) else "  (no data yet)"))
