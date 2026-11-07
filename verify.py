#!/usr/bin/env python3
"""Project verification for the First Will & Estate Basics Guide.

Runs entirely with the Python standard library. Checks:
  1. Required files exist.
  2. LICENSE contains the exact required copyright line.
  3. README credits Asdale Dynamics, LLC.
  4. Markdown: every relative markdown link resolves to a real file.
  5. HTML: balanced tags, doctype, title, lang; every #anchor target exists;
     referenced local assets (styles.css, app.js) exist.
  6. JavaScript syntax check via `node --check` when node is available.
  7. Secret scan: no API-key-shaped strings or private keys anywhere.
  8. Personal-data hygiene: no email addresses in content files.
  9. Charset hygiene: no stray CJK characters (catches paste-glitch typos).

Exit code 0 = all checks pass.
"""

import io
import os
import re
import subprocess
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.abspath(__file__))

REQUIRED_FILES = [
    "LICENSE",
    "README.md",
    "site/index.html",
    "site/styles.css",
    "site/app.js",
    "docs/index.md",
    "docs/01-why-plan-ahead.md",
    "docs/02-your-will.md",
    "docs/03-beneficiaries.md",
    "docs/04-powers-of-attorney.md",
    "docs/05-healthcare-directives.md",
    "docs/06-family-letter-of-instruction.md",
    "docs/07-document-checklist.md",
    "docs/08-safe-storage.md",
    "docs/09-getting-help.md",
    "docs/glossary.md",
]

REQUIRED_COPYRIGHT = "Copyright (c) 2026 Asdale Dynamics, LLC"

SECRETS_PATTERNS = [
    r"AKIA[0-9A-Z]{16}",                      # AWS access key id
    r"sk-[A-Za-z0-9_-]{20,}",                 # generic sk- secret
    r"gh[pousr]_[A-Za-z0-9]{20,}",            # GitHub tokens
    r"xox[baprs]-[A-Za-z0-9-]{10,}",          # Slack tokens
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",    # private key blocks
    r"api[_-]?key\s*[:=]\s*['\"][A-Za-z0-9]",
    r"secret\s*[:=]\s*['\"][A-Za-z0-9]{8,}",
]

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
CJK_RE = re.compile(r"[\u3000-\u9fff\uff00-\uffef\u3400-\u4dbf]")

MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
HTML_ANCHOR_RE = re.compile(r'href="#([^"]+)"')


def read_text(path):
    with io.open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def find_files():
    found, missing = [], []
    for rel in REQUIRED_FILES:
        full = os.path.join(ROOT, rel)
        (found if os.path.isfile(full) else missing).append(rel)
    return found, missing


def check_license(issues):
    text = read_text(os.path.join(ROOT, "LICENSE"))
    if REQUIRED_COPYRIGHT not in text:
        issues.append(
            "LICENSE is missing the exact line: %s" % REQUIRED_COPYRIGHT
        )


def check_readme(issues):
    text = read_text(os.path.join(ROOT, "README.md"))
    if "Asdale Dynamics, LLC" not in text:
        issues.append("README does not credit Asdale Dynamics, LLC")


def collect_anchor_targets(html):
    return set(re.findall(r'<a[^>]+id="([^"]+)"', html)) | set(
        re.findall(r'id="([^"]+)"', html)
    )


class TagBalanceParser(HTMLParser):
    VOID_ELEMENTS = {
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "source", "track", "wbr",
    }

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []
        self.title_found = False
        self.lang_found = False

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.title_found = True
        attr_names = {k for k, _ in attrs}
        if tag == "html" and "lang" in attr_names:
            self.lang_found = True
        if tag not in self.VOID_ELEMENTS:
            self.stack.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if not self.stack:
            self.errors.append(
                "line %d: closing </%s> with empty stack" % (self.getpos()[0], tag)
            )
            return
        if tag in self.VOID_ELEMENTS:
            return
        while self.stack and self.stack[-1][0] != tag:
            self.stack.pop()
        if self.stack:
            self.stack.pop()
        else:
            self.errors.append(
                "line %d: unmatched closing </%s>" % (self.getpos()[0], tag)
            )


def check_markdown_links(issues):
    for rel in [f for f in REQUIRED_FILES if f.endswith(".md")]:
        full = os.path.join(ROOT, rel)
        text = read_text(full)
        for match in MD_LINK_RE.finditer(text):
            target = match.group(1).strip()
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            path_part = target.split("#")[0]
            if path_part:
                resolved = os.path.normpath(
                    os.path.join(os.path.dirname(full), path_part)
                )
                if not os.path.isfile(resolved):
                    issues.append(
                        "%s: broken markdown link -> %s" % (rel, target)
                    )


def check_html(issues):
    full = os.path.join(ROOT, "site", "index.html")
    html = read_text(full)

    if not html.lstrip().lower().startswith("<!doctype html>"):
        issues.append("site/index.html: missing doctype")

    parser = TagBalanceParser()
    try:
        parser.feed(html)
        parser.close()
    except Exception as exc:  # noqa: BLE001 - report any parse failure
        issues.append("site/index.html: parse error: %s" % exc)
        return

    for err in parser.errors:
        issues.append("site/index.html: %s" % err)
    for tag, pos in parser.stack:
        issues.append(
            "site/index.html: unclosed <{tag}> opened on line {line}".format(
                tag=tag, line=pos[0]
            )
        )
    if not parser.title_found:
        issues.append("site/index.html: missing <title>")
    if not parser.lang_found:
        issues.append("site/index.html: missing lang attribute on <html>")

    anchors = collect_anchor_targets(html)
    for match in HTML_ANCHOR_RE.finditer(html):
        target = match.group(1)
        if target and target not in anchors:
            issues.append("site/index.html: href '#%s' has no target" % target)

    for asset in ("styles.css", "app.js"):
        expected = r"(?:href|src)=\"%s\"" % asset
        if not re.search(expected, html) and not re.search(
            r"(?:href|src)=.{1,5}%s" % re.escape(asset), html
        ):
            issues.append("site/index.html: does not reference %s" % asset)
        if not os.path.isfile(os.path.join(ROOT, "site", asset)):
            issues.append("site/%s referenced but missing" % asset)


def check_js(issues, warnings):
    node = prefs_node()
    if node is None:
        warnings.append(
            "node not found; skipped javascript syntax check "
            "(checked abbreviation only)"
        )
        return
    for js in ("site/app.js",):
        proc = subprocess.run(
            [node, "--check", os.path.join(ROOT, js)],
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            issues.append("%s: node --check failed: %s" % (js, proc.stderr.strip()))


def prefs_node():
    env_path = os.environ.get("PATH", "")
    for entry in env_path.split(os.pathsep):
        candidate = os.path.join(entry, "node")
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    return None


def scan_text_for_patterns(issues):
    scan_files = [
        f for f in REQUIRED_FILES
        if f.endswith((".md", ".html", ".css", ".js"))
    ]
    for rel in scan_files:
        text = read_text(os.path.join(ROOT, rel))
        for pattern in SECRETS_PATTERNS:
            if re.search(pattern, text):
                issues.append("%s: possible secret matching pattern %r" % (rel, pattern))
        for match in EMAIL_RE.finditer(text):
            issues.append("%s: possible personal data (email): %s" % (rel, match.group(0)))
        for match in CJK_RE.finditer(text):
            issues.append(
                "%s: stray CJK character %r near: %s"
                % (rel, match.group(0), text[max(0, match.start() - 30):match.end() + 30])
            )


# Known glitch strings that have appeared from bad pastes; keep checked
# so they can never land quietly again.
GLITCH_STRINGS = [
    "BeneficiaryDesignations",
    "cover_.",
    "\u86ed",
    "\u671d",
    "time\u538b\u529b",
    "theNetflix",
    "the\u671d",
    "Saannidity",
    "consuIt",
    "in_coef",
    "tranquil-late",
    "\u56ed\u827a",
    "note that#",
]


def check_glitch_strings(issues):
    scan_files = [
        f for f in REQUIRED_FILES
        if f.endswith((".md", ".html", ".css", ".js"))
    ]
    for rel in scan_files:
        text = read_text(os.path.join(ROOT, rel))
        for glitch in GLITCH_STRINGS:
            if glitch in text:
                issues.append(
                    "%s: known glitch string present: %r" % (rel, glitch)
                )


def check_no_network_dependencies(issues):
    html = read_text(os.path.join(ROOT, "site", "index.html"))
    if re.search(r'<script[^>]+src="https?://', html):
        issues.append("site/index.html: external script reference (must be local-only)")
    if re.search(r'<link[^>]+href="https?://', html):
        issues.append("site/index.html: external stylesheet reference (must be local-only)")
    js = read_text(os.path.join(ROOT, "site", "app.js"))
    if re.search(r"(fetch|XMLHttpRequest|WebSocket)\s*\(", js):
        issues.append("site/app.js: network call detected (must be local-only)")


def main():
    issues, warnings = [], []

    found, missing = find_files()
    for rel in found:
        print("  ok: %s" % rel)
    for rel in missing:
        issues.append("missing required file: %s" % rel)

    check_license(issues)
    check_readme(issues)
    check_markdown_links(issues)
    check_html(issues)
    check_js(issues, warnings)
    check_no_network_dependencies(issues)
    scan_text_for_patterns(issues)
    check_glitch_strings(issues)

    print()
    for warning in warnings:
        print("WARN: %s" % warning)
    if issues:
        print("FAILED with %d issue(s):" % len(issues))
        for issue in issues:
            print("  - %s" % issue)
        return 1
    print("All checks passed (%d files verified)." % len(REQUIRED_FILES))
    return 0


if __name__ == "__main__":
    sys.exit(main())
