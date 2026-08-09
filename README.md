# 🏛 Government-Scheme Eligibility Assistant

A **100% local, offline** Python desktop app that explains public-benefit
government schemes, checks your likely eligibility, lists required
documents, and shows you how to apply — all through a colorful,
high-contrast, easy-to-read Tkinter dashboard.

No internet connection, no API keys, no cloud calls. Everything — the
scheme database, the eligibility logic, and your check history — runs
and stays on your machine.

## Features
- 📝 Simple eligibility form (age, gender, occupation, income, location, key flags)
- ⚖ Rule-based local eligibility engine — scores every scheme by percentage match
- ✅ Results tab: color-coded badges (Likely / Possibly / Unlikely Eligible)
- 📄 Full list of required documents per scheme
- 💰 Benefit amount + how to apply, in plain language
- ⚠ "Gaps to address" explaining exactly why you didn't fully qualify
- 📚 Browse-all-schemes tab, independent of your personal data
- 🕓 Local history tab — every check is saved to `eligibility_history.json`
- 🎨 High-contrast colorful UI — dark header, white content cards, all text clearly readable

## Setup
```bash
pip install -r requirements.txt   # no external packages needed
python scheme_assistant_app.py
```

Requires Python 3.8+ with Tkinter (bundled with standard Python on
Windows/macOS; on Linux run `sudo apt-get install python3-tk` if missing).

## How eligibility scoring works
1. Each scheme in `schemes_data.py` defines its own criteria (age range,
   income ceiling, occupation, gender, location, and boolean flags like
   land ownership or BPL card).
2. `eligibility_engine.py` compares your entered profile against every
   scheme's criteria and computes a **match percentage**.
3. Schemes are bucketed as:
   - **Likely Eligible** — 80%+ of criteria matched
   - **Possibly Eligible** — 50–79% matched
   - **Unlikely Eligible** — below 50%
4. Any unmet condition is listed as a "gap to address" so you know
   exactly what's missing.

## Adding more schemes
Open `schemes_data.py` and append a new dictionary to the `SCHEMES` list
following the same structure (`name`, `category`, `description`,
`criteria`, `documents`, `benefit`, `apply_mode`). No other code changes
needed — the form and results screens pick up new schemes automatically.

## Files
- `scheme_assistant_app.py` — main application (UI + orchestration)
- `schemes_data.py` — local scheme database (editable, offline)
- `eligibility_engine.py` — rule-based matching logic
- `eligibility_history.json` — auto-created after your first check
- `requirements.txt` — dependencies (none beyond standard library)

## Disclaimer
This tool provides an **indicative** eligibility estimate based on
publicly available scheme criteria. It is not an official government
application and does not guarantee approval. Always verify final
eligibility and required documents with the relevant government
department or official portal before applying.
