# FGLLID site data

## Files

| File | Purpose |
|------|---------|
| `site.json` | Main editable site content (hotline, DG, deputies, services, offices, media, publications, gallery) |
| `news.json` | News feed (from `scripts/fetch_news.py`) |

## Admin (no typing required)

1. Open `admin.html` (use a local server, e.g. `npx serve .`).
2. **Drop files** onto the import zone:
   - `.json` → replaces / merges site data
   - images (`.jpg` `.png` `.webp` …) → added to **Gallery** (or DG photo if filename starts with `dg`)
   - `.txt` / `.md` → added to **Publications**
3. Click **Save (local)** → stored in browser `localStorage` → `index.html` shows it.
4. Click **Export site.json** → download and overwrite `data/site.json` for permanent/static hosting.

## Schema (site.json)

See `site.json` for the live structure. Top-level keys:

- `hotline`, `dg`, `deputies[]`, `services[]`, `offices[]`, `media[]`, `publications[]`, `gallery[]`
