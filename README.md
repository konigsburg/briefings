# Daily Briefings

Self-updating home-screen app. `index.html` is the shell; it fetches
`data/today.json` (latest brief) and `data/archive.json` (past briefs +
inbox summaries) on load, falling back to an embedded snapshot if they're absent.

Served via GitHub Pages at: https://<username>.github.io/briefings/

The 8:00 AM scheduled task overwrites `data/today.json` and appends to
`data/archive.json` each morning, so the home-screen icon auto-updates.
