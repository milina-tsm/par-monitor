TSM · KeHE PAR Supply Monitor
Static dashboard for the weekly KeHE PAR report from Green Spoon. Built for GitHub Pages — no backend, no build step. Each week's report becomes a JSON file; the dashboard charts trends automatically as weeks accumulate.
What it shows
KPI strip — requested demand ($/units), OOS lines, compliance %, delayed orders, est. units short
Supply grid — SKU × DC matrix, worst status per cell (the main view: spot supply risk in one glance)
Event calendar — ads, resets, new item launches with dates, PO deadlines, and a LIVE NOW flag
Compliance & RYG — KeHE's own flags rolled up
Top supply alerts — worst lines, sorted by delay
Week-over-week trends — activates automatically once 2+ weeks are loaded
First deploy
Create a GitHub repo (e.g. par-monitor), push this folder
Repo → Settings → Pages → Source: main branch, / (root)
Dashboard goes live at https://<user>.github.io/par-monitor/
Weekly update (≈1 minute)
# 1. save the new PAR xlsx from Green Spoon's email anywhere
# 2. convert it:
python update_data.py ~/Downloads/True_Sea_Moss_06_15_2026_PAR_Weekly_GREEN_SPOON_SALES.xlsx

# 3. push:
git add data/ && git commit -m "PAR week 2026-06-15" && git push

The script reads the week date from the filename (MM_DD_YYYY). If the filename format changes, pass it explicitly:

python update_data.py file.xlsx --date 2026-06-15

Re-running for the same week overwrites that week's data (safe to re-run).
Local preview
Browsers block fetch() from file://, so open via a local server:

python -m http.server
# → http://localhost:8000
Requirements
Python 3 with pandas and openpyxl (pip install pandas openpyxl) — only for the converter; the dashboard itself is pure static HTML/JS
File layout
index.html        ← dashboard (don't need to touch)
update_data.py    ← weekly converter
data/
  manifest.json   ← auto-maintained list of weeks
  2026-06-08.json ← one file per week

