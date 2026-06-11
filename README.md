# TSM · KeHE PAR Supply Monitor

Dashboard for the weekly KeHE PAR report from Green Spoon. Lives on GitHub Pages. **No coding needed** — you upload the weekly Excel file through the GitHub website and everything else happens automatically.

---

## One-time setup (~10 minutes, all in the browser)

1. Go to **github.com** → click **+** (top right) → **New repository**
   - Name: `par-monitor` (or anything)
   - Choose **Private** if you don't want the data public
   - Click **Create repository**

2. On the new repo page click **"uploading an existing file"**
   - Drag in EVERYTHING from this folder (index.html, update_data.py, README.md, and the `data`, `incoming`, `processed`, `.github` folders)
   - If your computer hides the `.github` folder: upload the zip contents as-is, GitHub keeps the structure
   - Click **Commit changes**

3. Turn on the dashboard: **Settings** (top of repo) → **Pages** (left menu)
   - Source: **Deploy from a branch**
   - Branch: **main**, folder: **/ (root)** → **Save**
   - After ~1 minute your dashboard is live at the link shown on that page

4. Allow the robot to save data: **Settings** → **Actions** → **General**
   - Scroll to **Workflow permissions** → select **Read and write permissions** → **Save**

Done. You never need to touch this setup again.

---

## Every week (~1 minute, all in the browser)

1. Save the PAR file from Green Spoon's email to your computer
2. Open your repo on github.com → click the **`incoming`** folder
3. Click **Add file** → **Upload files** → drag the xlsx in → **Commit changes**
4. Wait ~1 minute. The robot converts the file, files it away in `processed/`, and the dashboard updates itself. Refresh the dashboard page — the new week appears in the dropdown, and trend charts appear once there are 2+ weeks.

That's it. No Python, no terminal, ever.

---

## If something goes wrong

- Repo → **Actions** tab shows each run. Green check = worked. Red X = click it to see the error (most common: filename doesn't contain the date as `MM_DD_YYYY` — rename the file like the original and re-upload).
- Uploading the same week again is safe — it just overwrites that week's numbers.

## What the dashboard shows

- **KPI strip** — demand $, OOS lines, compliance %, delayed orders, units short
- **Supply grid** — SKU × DC matrix, spot supply risk in one glance
- **Event calendar** — ads, resets, new item launches, with PO deadlines and a LIVE NOW flag
- **Top supply alerts** — worst lines first
- **Trends** — week-over-week once 2+ weeks are loaded
