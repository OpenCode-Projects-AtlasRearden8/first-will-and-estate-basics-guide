# First Will & Estate Basics Guide

A gentle, beginner-friendly manual for getting your advance-planning basics in order:
wills, beneficiaries, powers of attorney, healthcare directives, and a family letter
of instruction — written without gloom, with a document checklist and safe-storage
guidance.

**Education only. This is never legal advice.** For anything specific to your state,
country, family, or finances, this guide encourages you to work with a licensed
estate-planning attorney or a qualified professional. It explains the vocabulary and
the "what and why" so that conversation goes faster and costs less.

Published by **Asdale Dynamics, LLC** · Plain-English education, local-first.

## Who this is for

Anyone who has ever thought "I really should get a will someday" and then closed the
tab. If planning conversations feel heavy, this guide is deliberately built to feel
light: short sections, plain words, concrete next steps, zero doom.

## What's here

| Path | What it is |
| --- | --- |
| `docs/` | The full manual in Markdown — start at `docs/index.md` |
| `site/index.html` | A self-contained static HTML version of the guide (open it in any browser) |
| `verify.py` | Sanity checks: files, links, anchors, license line, secret scan |
| `STATUS.md` | Build status, run instructions, verification results, known gaps |

### The manual

1. [Start here](docs/index.md) — how to use this guide in small doses
2. [Why plan ahead](docs/01-why-plan-ahead.md) — planning as a gift, not a goodbye
3. [Your will](docs/02-your-will.md) — what it does, what it can't
4. [Beneficiaries](docs/03-beneficiaries.md) — where the money goes without a will
5. [Powers of attorney](docs/04-powers-of-attorney.md) — who acts if you can't
6. [Healthcare directives](docs/05-healthcare-directives.md) — your voice when you can't speak
7. [Family letter of instruction](docs/06-family-letter-of-instruction.md) — the friendly companion doc
8. [Document checklist](docs/07-document-checklist.md) — what to have, what to make
9. [Safe storage](docs/08-safe-storage.md) — where papers live so they can be found
10. [Getting help](docs/09-getting-help.md) — when (and how) to hire a pro
- [Glossary](docs/glossary.md) — plain-English definitions

## How to run it

Everything is local-first: no servers, accounts, uploads, or network calls.

- **Read the Markdown:** open `docs/index.md`.
- **Use the site:** open `site/index.html` directly in a browser (double-click it,
  or `file://`), or serve it locally:
  ```bash
  python3 -m http.server 8000 --directory site
  # then visit http://localhost:8000
  ```
- **Verify the project:** `python3 verify.py`

This project sells nothing, hosts nothing, and contains no secrets or personal data.
The related guides *bereavement-paperwork-guide* (helping survivors after a loss) and
*digital-legacy-handbook* (online accounts) cover different ground; this one covers
planning **before** anything happens.

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Asdale Dynamics, LLC.
