# STATUS

Last updated: 2026-11-07

## What was built

**First Will & Estate Basics Guide** — a gentle, beginner-friendly advance-planning
manual (wills, beneficiaries, powers of attorney, healthcare directives, family
letter of instruction, document checklist, safe storage, getting professional help,
plus a glossary), published by Asdale Dynamics, LLC as MIT-licensed educational
material. Education only — never legal advice; the guide repeatedly and explicitly
encourages licensed professionals for specifics.

Components:

- `docs/` — the full manual in Markdown (10 files: start-here, why-plan-ahead,
  your-will, beneficiaries, powers-of-attorney, healthcare-directives,
  family-letter-of-instruction, document-checklist, safe-storage, getting-help,
  glossary). Each chapter ends with a small "Your move" action box.
- `site/` — a self-contained static HTML version of the guide (`index.html`,
  `styles.css`, `app.js`). No frameworks, no CDNs, no external requests. Includes a
  clickable document checklist whose progress persists in the browser's
  localStorage (with a reset button), plus a print-friendly layout and a
  reduced-motion/skip-link accessibility baseline.
- `verify.py` — stdlib-only verification script (files, license line, README credit,
  markdown links, HTML tag balance/anchors, `node --check` on JS, secret scan,
  personal-data scan, charset glitch scan, local-only asset check).
- `LICENSE` — MIT, copyright line: `Copyright (c) 2026 Asdale Dynamics, LLC`.
- `README.md` — credits Asdale Dynamics, LLC; documents how to read/serve/verify.

Intentional scope boundaries (kept distinct from sibling projects):

- Not a survivor/sympathy guide (that is *bereavement-paperwork-guide*), and not an
  online-accounts guide (that is *digital-legacy-handbook*) — the README and site
  footer note the distinction.
- Sells nothing, hosts nothing, tracks nothing. Local-first. No secrets, API keys,
  or personal data anywhere in the repo (verified by `verify.py`).

## How to run it

- Read the manual: open `docs/index.md` (plain Markdown, readable anywhere).
- Use the site: open `site/index.html` directly in any browser, or serve it:
  ```bash
  python3 -m http.server 8000 --directory site
  # then visit http://localhost:8000
  ```
- Verify: `python3 verify.py`

## Verification results (all passing)

1. `python3 verify.py` — **all checks passed (16 files verified)**:
   - All 16 required files present.
   - LICENSE contains the exact line `Copyright (c) 2026 Asdale Dynamics, LLC`.
   - README credits Asdale Dynamics, LLC.
   - Every relative markdown link in docs resolves.
   - `site/index.html`: doctype/title/lang present, tags balanced, all `#anchor`
     hrefs have targets, referenced assets exist.
   - `site/app.js`: passes `node --check`.
   - No external (network) stylesheet/script references; no network calls in JS.
   - Secret-pattern scan, email (personal-data) scan, and stray-CJK/glitch-string
     scan all clean.
2. Runtime smoke test — served `site/` with `python3 -m http.server`:
   `index.html` (200, 34.6 KB), `styles.css` (200), `app.js` (200); page contains
   title, 4 checklist groups, 27 checkboxes.
3. No build step exists or is needed (static, local-first by design).

Git: repository initialized and committed locally with the existing git identity
(Dylan Asdale). Plain commit message, no trailers. Nothing pushed, no remote.

## Known gaps (honest list)

- **Not legal advice, on purpose.** The guide deliberately stops at vocabulary,
  concepts, and checklists; it does not attempt state-specific legal rules. State
  variation is called out repeatedly and routed to professionals/official state
  forms instead.
- **No state-specific form page.** A future enhancement could enumerate each US
  state's official advance-directive form URL. Deliberately omitted so nothing
  goes stale or wrong quietly.
- **Checklist progress is per-browser.** localStorage only; no export/sync —
  local-first by design, but a crossover with another device needs a re-check.
- **The site and the docs are two hand-maintained renditions of the same content.**
  There is no generator that compiles `docs/*.md` into the site; a small build
  step could make the two provably identical. Kept manual to stay dependency-free.
- Glossary covers common beginner vocabulary only; trust design, estate tax, and
  probate mechanics are intentionally shallow, with routing to professionals.
