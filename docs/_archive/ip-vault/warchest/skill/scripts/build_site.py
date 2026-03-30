#!/usr/bin/env python3
"""
War Chest Site Builder — GrowDirect Content Pack Generator

Reads manifest.json, converts .md sources to styled HTML pages,
and assembles a multi-page password-gated briefing site.

Usage:
    python build_site.py rebuild                     # Full rebuild
    python build_site.py update --section [slug]     # Update one section
    python build_site.py add --name "Name" --source path/to/file.md  # Add section
    python build_site.py remove --section [slug]     # Remove section
"""

import json
import os
import re
import sys
import shutil
import argparse
from datetime import datetime
from pathlib import Path

try:
    import markdown
    from markdown.extensions.tables import TableExtension
    from markdown.extensions.fenced_code import FencedCodeExtension
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False

# ── Paths ──
WARCHEST_ROOT = Path(__file__).resolve().parent.parent.parent  # _ALX/WarChest/
MANIFEST_PATH = WARCHEST_ROOT / "manifest.json"
SITE_DIR = WARCHEST_ROOT / "site"
ARCHIVE_DIR = WARCHEST_ROOT / "archive"
SOURCES_DIR = WARCHEST_ROOT / "sources"


# ── Design System ──
FONTS_IMPORT = "@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');"

CSS_VARS = """
:root {
  --btc: #F7931A;
  --gold: #FBBF24;
  --dark: #080808;
  --dim: #111111;
  --card: #141414;
  --border: #1e1e1e;
  --text: #E8E4DC;
  --muted: #8a8a8a;
  --faint: #222;
  --green: #22C55E;
  --red: #EF4444;
}
"""

BASE_CSS = """
* { margin:0; padding:0; box-sizing:border-box; }
html { scroll-behavior: smooth; }

body {
  background: var(--dark);
  color: var(--text);
  font-family: 'DM Sans', sans-serif;
  font-weight: 300;
  line-height: 1.7;
  overflow-x: hidden;
}

/* Grain overlay */
body::after {
  content:'';
  position:fixed;
  inset:0;
  pointer-events:none;
  z-index:2;
  opacity:0.02;
  background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}

/* Nav */
nav {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 100;
  background: rgba(8,8,8,0.92);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
  padding: 0 48px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-logo {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 22px;
  letter-spacing: 0.12em;
  background: linear-gradient(135deg, var(--btc), var(--gold));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-decoration: none;
  white-space: nowrap;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 20px;
  position: relative;
}

.nav-current {
  font-family: 'Space Mono', monospace;
  font-size: 10px;
  color: var(--muted);
  letter-spacing: 0.12em;
  text-transform: uppercase;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 300px;
}

.nav-toggle {
  font-family: 'Space Mono', monospace;
  font-size: 10px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--btc);
  background: none;
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 8px 16px;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.nav-toggle:hover {
  border-color: var(--btc);
  color: var(--gold);
}

/* Section dropdown menu */
.nav-dropdown {
  display: none;
  position: fixed;
  top: 60px;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 99;
  background: rgba(8,8,8,0.96);
  backdrop-filter: blur(16px);
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}

.nav-dropdown.open { display: block; }

.nav-dropdown-inner {
  max-width: 700px;
  margin: 0 auto;
  padding: 32px 48px 80px;
}

.nav-section-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-section-list li {
  border-bottom: 1px solid var(--border);
}

.nav-section-list a {
  display: flex;
  align-items: baseline;
  gap: 16px;
  padding: 14px 0;
  text-decoration: none;
  transition: all 0.2s;
}

.nav-section-list a:hover {
  padding-left: 8px;
}

.nav-section-num {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 20px;
  color: var(--btc);
  min-width: 32px;
}

.nav-section-name {
  font-family: 'DM Sans', sans-serif;
  font-size: 15px;
  font-weight: 500;
  color: var(--text);
  transition: color 0.2s;
}

.nav-section-list a:hover .nav-section-name,
.nav-section-list a.active .nav-section-name {
  color: var(--gold);
}

.nav-section-list a.active .nav-section-num {
  color: var(--gold);
}

.nav-divider {
  font-family: 'Space Mono', monospace;
  font-size: 9px;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: var(--muted);
  padding: 24px 0 8px;
  border-bottom: none !important;
}

.nav-section-list li.nav-divider + li {
  border-top: none;
}

/* Main content */
main {
  max-width: 960px;
  margin: 0 auto;
  padding: 100px 32px 80px;
  position: relative;
  z-index: 3;
}

/* Typography */
h1 {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 56px;
  letter-spacing: 0.08em;
  background: linear-gradient(135deg, var(--btc), var(--gold));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 16px;
  line-height: 1.1;
}

h2 {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 36px;
  letter-spacing: 0.06em;
  color: var(--gold);
  margin-top: 48px;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border);
}

h3 {
  font-family: 'DM Sans', sans-serif;
  font-size: 20px;
  font-weight: 600;
  color: var(--text);
  margin-top: 32px;
  margin-bottom: 12px;
}

h4 {
  font-family: 'Space Mono', monospace;
  font-size: 12px;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--btc);
  margin-top: 24px;
  margin-bottom: 8px;
}

p {
  margin-bottom: 20px;
  font-size: 16px;
}

a { color: var(--btc); text-decoration: none; transition: color 0.2s; }
a:hover { color: var(--gold); }

strong { font-weight: 600; color: var(--text); }
em { font-style: italic; }

/* Lists */
ul, ol {
  margin: 0 0 20px 24px;
  font-size: 16px;
}

li {
  margin-bottom: 8px;
  line-height: 1.7;
}

/* Blockquote */
blockquote {
  border-left: 3px solid var(--btc);
  padding: 20px 28px;
  margin: 32px 0;
  background: rgba(247,147,26,0.03);
  font-family: 'DM Serif Display', serif;
  font-style: italic;
  font-size: 18px;
  line-height: 1.6;
  color: var(--text);
}

/* Code */
code {
  font-family: 'Space Mono', monospace;
  font-size: 13px;
  background: var(--dim);
  padding: 2px 8px;
  border-radius: 3px;
  color: var(--btc);
}

pre {
  background: var(--dim);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 20px 24px;
  margin: 24px 0;
  overflow-x: auto;
}

pre code {
  background: none;
  padding: 0;
  font-size: 13px;
  color: var(--text);
  line-height: 1.6;
}

/* Tables */
table {
  width: 100%;
  border-collapse: collapse;
  margin: 24px 0;
  font-size: 14px;
}

th {
  font-family: 'Space Mono', monospace;
  font-size: 10px;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--btc);
  text-align: left;
  padding: 12px 16px;
  border-bottom: 2px solid var(--border);
  background: var(--dim);
}

td {
  padding: 12px 16px;
  border-bottom: 1px solid var(--border);
  color: var(--text);
}

tr:hover td { background: rgba(247,147,26,0.02); }

/* Cards */
.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 28px;
  margin: 20px 0;
}

/* Horizontal rule */
hr {
  border: none;
  border-top: 1px solid var(--border);
  margin: 48px 0;
}

/* Section label */
.section-label {
  font-family: 'Space Mono', monospace;
  font-size: 10px;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 8px;
}

/* Prev / Next page navigation */
.page-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 64px;
  padding-top: 32px;
  border-top: 1px solid var(--border);
}

.page-nav a {
  font-family: 'Space Mono', monospace;
  font-size: 11px;
  color: var(--muted);
  text-decoration: none;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  transition: color 0.2s;
  max-width: 45%;
}

.page-nav a:hover { color: var(--gold); }
.page-nav .prev::before { content: '\\2190  '; }
.page-nav .next::after { content: '  \\2192'; }

/* Utility footer links */
.footer-utils {
  display: flex;
  justify-content: center;
  gap: 32px;
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid var(--border);
  flex-wrap: wrap;
}

.footer-utils a {
  font-family: 'Space Mono', monospace;
  font-size: 9px;
  color: var(--muted);
  text-decoration: none;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  transition: color 0.2s;
}

.footer-utils a:hover { color: var(--btc); }

/* Footer */
footer {
  max-width: 960px;
  margin: 0 auto;
  padding: 48px 32px;
  border-top: 1px solid var(--border);
  text-align: center;
  position: relative;
  z-index: 3;
}

footer p {
  font-family: 'Space Mono', monospace;
  font-size: 10px;
  color: var(--muted);
  letter-spacing: 0.15em;
  text-transform: uppercase;
  margin-bottom: 8px;
}

footer .version {
  color: var(--btc);
}

/* Embed iframe for interactive pages */
.embed-frame {
  width: 100%;
  min-height: 80vh;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: var(--dim);
}

/* Responsive */
@media (max-width: 768px) {
  nav { padding: 0 20px; height: 50px; }
  .nav-current { display: none; }
  .nav-toggle { font-size: 9px; padding: 6px 12px; }
  .nav-dropdown-inner { padding: 20px; }
  main { padding: 80px 20px 60px; }
  h1 { font-size: 36px; }
  h2 { font-size: 28px; }
  .page-nav { flex-direction: column; gap: 16px; }
  .page-nav a { max-width: 100%; text-align: center; }
  .embed-frame { min-height: 60vh; }
}
"""

# ── Gate HTML ──
GATE_CSS = """
#gate {
  position: fixed;
  inset: 0;
  background: var(--dark);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 32px;
}

.gate-logo {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 52px;
  letter-spacing: 0.12em;
  background: linear-gradient(135deg, var(--btc), var(--gold));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.gate-sub {
  font-family: 'Space Mono', monospace;
  font-size: 10px;
  color: var(--muted);
  letter-spacing: 0.25em;
  text-transform: uppercase;
  text-align: center;
}

.gate-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  width: 280px;
}

.gate-input {
  width: 100%;
  background: var(--dim);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 14px 18px;
  color: var(--text);
  font-family: 'Space Mono', monospace;
  font-size: 14px;
  letter-spacing: 0.15em;
  text-align: center;
  outline: none;
  transition: border-color 0.2s;
}

.gate-input:focus { border-color: var(--btc); }
.gate-input::placeholder { color: var(--muted); }

.gate-btn {
  width: 100%;
  background: linear-gradient(135deg, var(--btc), var(--gold));
  border: none;
  border-radius: 4px;
  padding: 14px;
  font-family: 'Bebas Neue', sans-serif;
  font-size: 18px;
  letter-spacing: 0.12em;
  color: #000;
  cursor: pointer;
  transition: opacity 0.2s;
}

.gate-btn:hover { opacity: 0.85; }

.gate-error {
  font-family: 'Space Mono', monospace;
  font-size: 10px;
  color: var(--red);
  letter-spacing: 0.1em;
  display: none;
}

.gate-disclaimer {
  font-size: 10px;
  color: var(--muted);
  text-align: center;
  max-width: 260px;
  line-height: 1.6;
}
"""

# ── Index-only supplemental CSS ──
INDEX_CSS = """
#site { display: none; }

.toc {
  max-width: 700px;
  margin: 60px auto;
}

.toc-item {
  display: grid;
  grid-template-columns: 48px 1fr;
  grid-template-rows: auto auto;
  gap: 0 16px;
  padding: 20px 0;
  border-bottom: 1px solid var(--border);
  text-decoration: none;
  transition: all 0.2s;
}

.toc-item:hover {
  padding-left: 8px;
}

.toc-item:hover .toc-name {
  color: var(--gold);
}

.toc-num {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 28px;
  color: var(--btc);
  grid-row: 1 / 3;
  display: flex;
  align-items: center;
}

.toc-name {
  font-family: 'DM Sans', sans-serif;
  font-size: 18px;
  font-weight: 600;
  color: var(--text);
  transition: color 0.2s;
}

.toc-desc {
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  color: var(--muted);
  line-height: 1.5;
}

.index-header {
  text-align: center;
  padding: 80px 0 40px;
}

/* Utility section in TOC */
.toc-utility {
  margin-top: 48px;
  padding-top: 32px;
  border-top: 1px solid var(--border);
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}

.toc-utility-label {
  font-family: 'Space Mono', monospace;
  font-size: 10px;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 16px;
}

.toc-utility-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.toc-util-link {
  display: block;
  padding: 16px 20px;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 6px;
  text-decoration: none;
  transition: border-color 0.2s;
}

.toc-util-link:hover { border-color: var(--btc); }

.toc-util-link .toc-name {
  font-size: 15px;
}

.toc-util-link .toc-desc {
  font-size: 12px;
  margin-top: 4px;
}

@media (max-width: 768px) {
  .toc-utility-grid { grid-template-columns: 1fr; }
}
"""


def load_manifest():
    with open(MANIFEST_PATH, 'r') as f:
        return json.load(f)


def save_manifest(manifest):
    with open(MANIFEST_PATH, 'w') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)


def md_to_html(md_text):
    """Convert markdown text to HTML."""
    if HAS_MARKDOWN:
        md = markdown.Markdown(extensions=[
            'tables',
            'fenced_code',
            'nl2br',
        ])
        return md.convert(md_text)
    else:
        # Fallback: basic conversion
        import re
        html = md_text
        # Headers
        html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        # Bold and italic
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
        # Blockquotes
        lines = html.split('\n')
        result = []
        in_quote = False
        for line in lines:
            if line.startswith('> '):
                if not in_quote:
                    result.append('<blockquote>')
                    in_quote = True
                result.append(line[2:])
            else:
                if in_quote:
                    result.append('</blockquote>')
                    in_quote = False
                result.append(line)
        if in_quote:
            result.append('</blockquote>')
        html = '\n'.join(result)
        # Paragraphs
        html = re.sub(r'\n\n+', '</p>\n<p>', html)
        html = f'<p>{html}</p>'
        html = re.sub(r'<p>(<h[1-4]>)', r'\1', html)
        html = re.sub(r'(</h[1-4]>)</p>', r'\1', html)
        html = re.sub(r'<p>(<blockquote>)', r'\1', html)
        html = re.sub(r'(</blockquote>)</p>', r'\1', html)
        return html


def extract_content(source_path, extract_type, heading=None):
    """Extract specific content region from a markdown source file.

    Args:
        source_path: Path to the .md file
        extract_type: One of 'first_paragraph', 'heading_paragraph',
                      'heading_blockquote', 'heading_prose'
        heading: Required for heading_* extract types

    Returns:
        str: HTML string of the extracted content, or empty string if not found
    """
    if not source_path.exists():
        return ''

    text = source_path.read_text()
    lines = text.split('\n')

    if extract_type == 'first_paragraph':
        # Skip title line (# ...) and metadata, collect until ## or ---
        # If nothing found before first --- or ##, fall through to first
        # paragraph under the first ## heading.
        paragraphs = []
        in_content = False
        hit_divider = False
        first_heading = None
        for line in lines:
            if line.startswith('# ') and not line.startswith('## ') and not in_content:
                in_content = True
                continue
            if in_content:
                if line.startswith('## ') or line.strip() == '---':
                    hit_divider = True
                    if line.startswith('## '):
                        first_heading = line.lstrip('#').strip()
                    break
                if line.startswith('> '):
                    continue
                if line.startswith('*Spine:') or line.startswith('**Status:**'):
                    continue
                paragraphs.append(line)
        content = '\n'.join(paragraphs).strip()
        blocks = [b.strip() for b in content.split('\n\n') if b.strip()]
        content = blocks[0] if blocks else ''
        if content:
            return md_to_html(content)
        # Fallback: if no content before divider, grab first paragraph
        # after the first ## heading
        if hit_divider:
            past_divider = False
            past_heading = False
            fallback = []
            for line in lines:
                if not past_divider:
                    if line.strip() == '---' or line.startswith('## '):
                        past_divider = True
                        if line.startswith('## '):
                            past_heading = True
                        continue
                elif not past_heading:
                    if line.startswith('## '):
                        past_heading = True
                    continue
                else:
                    if line.startswith('## ') or line.strip() == '---':
                        break
                    if line.startswith('### '):
                        break
                    if line.startswith('> '):
                        continue
                    fallback.append(line)
            content = '\n'.join(fallback).strip()
            blocks = [b.strip() for b in content.split('\n\n') if b.strip()]
            content = blocks[0] if blocks else ''
            return md_to_html(content) if content else ''
        return ''

    elif extract_type == 'heading_paragraph':
        # Find ## {heading}, take first paragraph after it
        found = False
        paragraphs = []
        for line in lines:
            if line.startswith('## ') and heading and heading in line:
                found = True
                continue
            if found:
                if line.startswith('## ') or line.strip() == '---':
                    break
                if line.startswith('### '):
                    break
                paragraphs.append(line)
        content = '\n'.join(paragraphs).strip()
        blocks = [b.strip() for b in content.split('\n\n') if b.strip()]
        content = blocks[0] if blocks else ''
        return md_to_html(content) if content else ''

    elif extract_type == 'heading_blockquote':
        # Find ## heading containing {heading}, take first blockquote
        found = False
        quote_lines = []
        for line in lines:
            if line.startswith('## ') and heading and heading in line:
                found = True
                continue
            if found:
                if line.startswith('> '):
                    quote_lines.append(line[2:].strip())
                elif quote_lines:
                    break
        content = ' '.join(quote_lines).strip()
        # Strip surrounding *...* and quotes
        content = content.strip('*').strip().strip('"').strip("'")
        return content  # Raw text for pull-quote — no <p> wrapping

    elif extract_type == 'heading_prose':
        # Find ## heading containing {heading}, take all paragraphs
        # (excluding blockquotes) until next --- or ##
        found = False
        prose = []
        for line in lines:
            if line.startswith('## ') and heading and heading in line:
                found = True
                continue
            if found:
                if line.startswith('## ') or line.strip() == '---':
                    break
                if line.startswith('> '):
                    continue
                prose.append(line)
        content = '\n'.join(prose).strip()
        if not content:
            return ''
        # Convert paragraphs to <p> tags
        blocks = [b.strip() for b in content.split('\n\n') if b.strip()]
        html_parts = []
        for block in blocks:
            converted = md_to_html(block)
            # Ensure wrapped in <p> if not already
            if not converted.strip().startswith('<'):
                converted = f'<p>{converted}</p>'
            html_parts.append(converted)
        return '\n'.join(html_parts)

    return ''


# Regex for matching content markers in the investor template
CONTENT_MARKER_RE = re.compile(
    r'(<!-- CONTENT:(\S+?) -->).*?(<!-- /CONTENT:\2 -->)',
    re.DOTALL
)


def get_content_sections(manifest):
    """Get non-utility sections in the pack feed, ordered."""
    return sorted(
        [s for s in manifest['sections']
         if 'pack' in s.get('feeds', []) and not s.get('utility')],
        key=lambda s: s['order']
    )


def get_utility_sections(manifest):
    """Get utility sections in the pack feed, ordered."""
    return sorted(
        [s for s in manifest['sections']
         if 'pack' in s.get('feeds', []) and s.get('utility')],
        key=lambda s: s['order']
    )


def build_nav(manifest, active_slug=None, active_name=None):
    """Generate navigation HTML with dropdown section menu."""
    content_sections = get_content_sections(manifest)
    utility_sections = get_utility_sections(manifest)

    # Build section list items
    section_items = []
    for idx, section in enumerate(content_sections, 1):
        active_cls = ' class="active"' if section['slug'] == active_slug else ''
        section_items.append(
            f'<li><a href="{section["slug"]}.html"{active_cls}>'
            f'<span class="nav-section-num">{idx:02d}</span>'
            f'<span class="nav-section-name">{section["name"]}</span></a></li>'
        )

    # Add utility divider + items
    if utility_sections:
        section_items.append('<li class="nav-divider">Reference &amp; Governance</li>')
        for section in utility_sections:
            active_cls = ' class="active"' if section['slug'] == active_slug else ''
            section_items.append(
                f'<li><a href="{section["slug"]}.html"{active_cls}>'
                f'<span class="nav-section-num">&mdash;</span>'
                f'<span class="nav-section-name">{section["name"]}</span></a></li>'
            )

    # Current section display
    current_display = f'<span class="nav-current">{active_name}</span>' if active_name else ''

    nav_html = f'''<nav>
  <a href="index.html" class="nav-logo">GROWDIRECT</a>
  <div class="nav-right">
    {current_display}
    <button class="nav-toggle" onclick="document.getElementById('navDrop').classList.toggle('open');this.textContent=this.textContent==='SECTIONS'?'CLOSE':'SECTIONS'" aria-label="Toggle section menu">SECTIONS</button>
  </div>
</nav>
<div id="navDrop" class="nav-dropdown" onclick="if(event.target===this){{this.classList.remove('open');document.querySelector('.nav-toggle').textContent='SECTIONS'}}">
  <div class="nav-dropdown-inner">
    <ul class="nav-section-list">
      {"".join(section_items)}
    </ul>
  </div>
</div>'''
    return nav_html


def build_utility_footer(manifest):
    """Generate utility page links for the footer."""
    utils = get_utility_sections(manifest)
    if not utils:
        return ''
    links = ' &middot; '.join(
        f'<a href="{s["slug"]}.html">{s["name"]}</a>'
        for s in utils
    )
    return f'<div class="footer-utils">{links}</div>'


def build_page_nav(prev_section, next_section):
    """Generate prev/next page navigation."""
    if not prev_section and not next_section:
        return ''
    prev_link = (
        f'<a class="prev" href="{prev_section["slug"]}.html">{prev_section["name"]}</a>'
        if prev_section else '<span></span>'
    )
    next_link = (
        f'<a class="next" href="{next_section["slug"]}.html">{next_section["name"]}</a>'
        if next_section else '<span></span>'
    )
    return f'<div class="page-nav">{prev_link}{next_link}</div>'


def build_auth_script():
    """Generate session auth check script for section pages."""
    return '''<script>
if(!sessionStorage.getItem('wc_auth')){
  window.location.href='index.html?r='+encodeURIComponent(window.location.pathname.split('/').pop());
}
</script>'''


def build_page(manifest, section, content_html, prev_section=None, next_section=None):
    """Wrap content in full page template with auth check, nav, prev/next."""
    nav = build_nav(manifest, active_slug=section['slug'], active_name=section['name'])
    version = manifest.get('version', '0.1')
    now = datetime.now().strftime('%B %d, %Y')
    auth_script = build_auth_script()
    page_nav = build_page_nav(prev_section, next_section)
    util_footer = build_utility_footer(manifest)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{section['name']} — GrowDirect Private Briefing</title>
<style>
{FONTS_IMPORT}
{CSS_VARS}
{BASE_CSS}
</style>
</head>
<body>
{auth_script}
{nav}
<main>
  <div class="section-label">{section['order']:02d} — {section.get('audience', 'internal').upper()}</div>
  <h1>{section['name']}</h1>
  {content_html}
  {page_nav}
</main>
<footer>
  <p>GrowDirect &middot; Canary LP &middot; Confidential &middot; {now}</p>
  <p class="version">War Chest v{version} &middot; Patent Pending — Provisional 63/991,596</p>
  {util_footer}
</footer>
</body>
</html>'''


def build_index(manifest):
    """Build the index page with password gate, nav, TOC, and utility section."""
    password = manifest.get('password', 'eljeffe2026')
    version = manifest.get('version', '0.1')
    now = datetime.now().strftime('%B %d, %Y')

    # Content TOC items
    toc_items = []
    content_sections = get_content_sections(manifest)
    for idx, section in enumerate(content_sections, 1):
        toc_items.append(f'''
        <a href="{section['slug']}.html" class="toc-item">
          <span class="toc-num">{idx:02d}</span>
          <span class="toc-name">{section['name']}</span>
          <span class="toc-desc">{section['description']}</span>
        </a>''')

    # Utility TOC items
    utility_sections = get_utility_sections(manifest)
    util_toc = ''
    if utility_sections:
        util_items = []
        for section in utility_sections:
            util_items.append(f'''
            <a href="{section['slug']}.html" class="toc-util-link">
              <span class="toc-name">{section['name']}</span>
              <span class="toc-desc">{section['description']}</span>
            </a>''')
        util_toc = f'''
    <div class="toc-utility">
      <div class="toc-utility-label">Reference &amp; Governance</div>
      <div class="toc-utility-grid">
        {"".join(util_items)}
      </div>
    </div>'''

    # Utility footer (same as section pages)
    util_footer = build_utility_footer(manifest)

    # Nav bar (shown after login)
    nav = build_nav(manifest)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GrowDirect — Private Briefing</title>
<style>
{FONTS_IMPORT}
{CSS_VARS}
{BASE_CSS}
{GATE_CSS}
{INDEX_CSS}
</style>
</head>
<body>

<!-- PASSWORD GATE -->
<div id="gate">
  <div class="gate-logo">GROWDIRECT</div>
  <div class="gate-sub">Private Briefing &middot; Confidential</div>
  <div class="gate-form">
    <input type="password" class="gate-input" id="pw" placeholder="Enter access code" autofocus>
    <button class="gate-btn" onclick="tryGate()">ENTER</button>
    <div class="gate-error" id="err">Invalid access code</div>
  </div>
  <div class="gate-disclaimer">
    This briefing contains confidential information.<br>
    Unauthorized distribution is prohibited.
  </div>
</div>

<!-- SITE CONTENT (hidden until auth) -->
<div id="site">
  {nav}
  <div class="index-header" style="padding-top:120px;">
    <h1>Private Briefing</h1>
    <div class="section-label">War Chest v{version} &middot; {now}</div>
  </div>
  <div class="toc">
    {"".join(toc_items)}
  </div>
  {util_toc}
  <footer>
    <p>GrowDirect &middot; Canary LP &middot; Confidential &middot; {now}</p>
    <p class="version">War Chest v{version} &middot; Patent Pending — Provisional 63/991,596</p>
    {util_footer}
  </footer>
</div>

<script>
function tryGate() {{
  var pw = document.getElementById('pw').value;
  if (pw === '{password}') {{
    sessionStorage.setItem('wc_auth','1');
    document.getElementById('gate').style.display = 'none';
    document.getElementById('site').style.display = 'block';
    // Handle redirect from gated section pages
    var params = new URLSearchParams(window.location.search);
    var redirect = params.get('r');
    if (redirect && redirect.endsWith('.html')) {{
      window.location.href = redirect;
    }}
  }} else {{
    var err = document.getElementById('err');
    err.style.display = 'block';
    document.getElementById('pw').value = '';
    document.getElementById('pw').focus();
    setTimeout(function(){{ err.style.display = 'none'; }}, 2000);
  }}
}}
document.getElementById('pw').addEventListener('keypress', function(e) {{
  if (e.key === 'Enter') tryGate();
}});
// Auto-unlock if already authenticated this session
if (sessionStorage.getItem('wc_auth')) {{
  document.getElementById('gate').style.display = 'none';
  document.getElementById('site').style.display = 'block';
}}
</script>
</body>
</html>'''


def archive_current(manifest):
    """Archive current site before rebuild."""
    version = manifest.get('version', '0.1')
    archive_path = ARCHIVE_DIR / f"v{version}"
    if SITE_DIR.exists() and any(SITE_DIR.iterdir()):
        archive_path.mkdir(parents=True, exist_ok=True)
        for f in SITE_DIR.iterdir():
            if f.is_file():
                shutil.copy2(f, archive_path / f.name)
        print(f"  Archived current site to archive/v{version}/")


def increment_version(manifest):
    """Bump patch version."""
    parts = manifest['version'].split('.')
    if len(parts) == 2:
        major, minor = int(parts[0]), int(parts[1])
        manifest['version'] = f"{major}.{minor + 1}"
    else:
        manifest['version'] = "1.0"
    return manifest


def filter_sections(manifest, output='pack'):
    """Filter sections by output target using feeds array."""
    return [s for s in manifest['sections'] if output in s.get('feeds', [])]


def build_investor(manifest):
    """Build single-page investor site from template + War Chest sources.

    Reads the investor template HTML, replaces content markers with
    rendered markdown from mapped War Chest source files, and writes
    the result to the investor output directory.
    """
    print(f"\n  INVESTOR SITE BUILD")
    print(f"  ═══════════════════════════════════")

    investor_config = manifest.get('outputs', {}).get('investor', {})
    template_rel = investor_config.get('template', 'skill/templates/investor_template.html')
    template_path = WARCHEST_ROOT / template_rel
    section_map = investor_config.get('section_map', {})
    output_dir = WARCHEST_ROOT / investor_config.get('dir', 'outputs/investor/')

    if not template_path.exists():
        print(f"  ✗ Template not found: {template_path}")
        return

    if not section_map:
        print(f"  ✗ No section_map in manifest outputs.investor")
        return

    # Load template
    html = template_path.read_text()

    # Process each content marker
    replaced = 0
    skipped = 0

    for marker_id, config in section_map.items():
        source_path = WARCHEST_ROOT / config['source']
        extract_type = config['extract']
        heading = config.get('heading')

        content = extract_content(source_path, extract_type, heading)

        if not content:
            print(f"  - {marker_id}: source missing or empty ({config['source']})")
            skipped += 1
            continue

        # Replace content between markers
        pattern = re.compile(
            rf'(<!-- CONTENT:{re.escape(marker_id)} -->).*?(<!-- /CONTENT:{re.escape(marker_id)} -->)',
            re.DOTALL
        )

        new_html, count = pattern.subn(
            lambda m: f'{m.group(1)}\n{content}\n{m.group(2)}',
            html
        )

        if count > 0:
            html = new_html
            replaced += 1
            print(f"  ✓ {marker_id} ← {config['source']}")
        else:
            print(f"  ? {marker_id}: marker not found in template")
            skipped += 1

    # Update password from manifest
    password = manifest.get('password', 'eljeffe2026')
    html = html.replace("const CODE = 'eljeffe2026'", f"const CODE = '{password}'")

    # Update build timestamp
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    html = html.replace('© GrowDirect 2026', f'© GrowDirect 2026 · Built {now}')

    # Write output
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "index.html"
    output_path.write_text(html)

    # Update manifest version
    version = investor_config.get('version', '3.0')
    parts = version.split('.')
    if len(parts) == 2:
        major, minor = int(parts[0]), int(parts[1])
        investor_config['version'] = f"{major}.{minor + 1}"
    investor_config['last_built'] = datetime.now().isoformat()
    save_manifest(manifest)

    print(f"\n  ═══════════════════════════════════")
    print(f"  Replaced: {replaced} | Skipped: {skipped}")
    print(f"  Version: {investor_config['version']}")
    print(f"  Output: {output_path}")
    print(f"  ═══════════════════════════════════\n")


def rebuild(manifest):
    """Full rebuild of all sections."""
    print(f"\n  WAR CHEST REBUILD")
    print(f"  ═══════════════════════════════════")

    # Archive current
    archive_current(manifest)

    # Increment version
    manifest = increment_version(manifest)
    manifest['last_built'] = datetime.now().isoformat()

    # Ensure site dir exists (overwrite files in place — no delete needed)
    SITE_DIR.mkdir(parents=True, exist_ok=True)

    # Build index (uses pack-filtered sections)
    index_html = build_index(manifest)
    (SITE_DIR / "index.html").write_text(index_html)
    print(f"  ✓ index.html (gate + nav + table of contents)")

    # Get ordered sections for prev/next calculation
    all_pack = sorted(filter_sections(manifest, 'pack'), key=lambda s: s['order'])
    built = 0
    skipped = 0

    for i, section in enumerate(all_pack):
        prev_section = all_pack[i - 1] if i > 0 else None
        next_section = all_pack[i + 1] if i < len(all_pack) - 1 else None

        source_path = WARCHEST_ROOT / section['source']
        if not source_path.exists():
            print(f"  ✗ {section['slug']}.html — source missing: {section['source']}")
            skipped += 1
            # Write placeholder page
            placeholder = f"<div class='card'><p>Content pending — source file not yet created.</p><p><code>{section['source']}</code></p></div>"
            page_html = build_page(manifest, section, placeholder, prev_section, next_section)
            (SITE_DIR / f"{section['slug']}.html").write_text(page_html)
            continue

        source_text = source_path.read_text()

        # If source is .html, check for embed mode
        if source_path.suffix == '.html':
            if section.get('embed_mode') == 'full':
                # Full standalone HTML — save raw file as _embed, wrap in iframe
                embed_filename = f"_embed_{section['slug']}.html"
                (SITE_DIR / embed_filename).write_text(source_text)
                content_html = f'<iframe src="{embed_filename}" class="embed-frame" frameborder="0" scrolling="auto" allowfullscreen></iframe>'
                page_html = build_page(manifest, section, content_html, prev_section, next_section)
                (SITE_DIR / f"{section['slug']}.html").write_text(page_html)
            else:
                # Extract body content and wrap in page template
                import re
                body_match = re.search(r'<body[^>]*>(.*)</body>', source_text, re.DOTALL)
                if body_match:
                    content_html = body_match.group(1)
                else:
                    content_html = source_text
                # Also extract any inline styles from <style> tags
                style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', source_text, re.DOTALL)
                if style_blocks:
                    content_html = f'<style>{"".join(style_blocks)}</style>\n{content_html}'
                page_html = build_page(manifest, section, content_html, prev_section, next_section)
                (SITE_DIR / f"{section['slug']}.html").write_text(page_html)
        else:
            content_html = md_to_html(source_text)
            page_html = build_page(manifest, section, content_html, prev_section, next_section)
            (SITE_DIR / f"{section['slug']}.html").write_text(page_html)

        section['last_updated'] = datetime.now().strftime('%Y-%m-%d')
        built += 1
        print(f"  ✓ {section['slug']}.html ({section['name']})")

    # Save updated manifest
    save_manifest(manifest)

    print(f"\n  ═══════════════════════════════════")
    print(f"  Built: {built} | Skipped: {skipped} | Version: {manifest['version']}")
    print(f"  Output: {SITE_DIR}/")
    print(f"  ═══════════════════════════════════\n")

    return manifest


def update_section(manifest, slug):
    """Update a single section."""
    section = next((s for s in manifest['sections'] if s['slug'] == slug), None)
    if not section:
        print(f"  ✗ Section '{slug}' not found in manifest")
        return manifest

    source_path = WARCHEST_ROOT / section['source']
    if not source_path.exists():
        print(f"  ✗ Source missing: {section['source']}")
        return manifest

    # Calculate prev/next
    all_pack = sorted(filter_sections(manifest, 'pack'), key=lambda s: s['order'])
    idx = next((i for i, s in enumerate(all_pack) if s['slug'] == slug), None)
    prev_section = all_pack[idx - 1] if idx and idx > 0 else None
    next_section = all_pack[idx + 1] if idx is not None and idx < len(all_pack) - 1 else None

    source_text = source_path.read_text()

    if source_path.suffix == '.html' and section.get('embed_mode') == 'full':
        embed_filename = f"_embed_{section['slug']}.html"
        (SITE_DIR / embed_filename).write_text(source_text)
        content_html = f'<iframe src="{embed_filename}" class="embed-frame" frameborder="0" scrolling="auto" allowfullscreen></iframe>'
        page_html = build_page(manifest, section, content_html, prev_section, next_section)
        (SITE_DIR / f"{section['slug']}.html").write_text(page_html)
    elif source_path.suffix == '.html':
        import re
        body_match = re.search(r'<body[^>]*>(.*)</body>', source_text, re.DOTALL)
        content_html = body_match.group(1) if body_match else source_text
        style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', source_text, re.DOTALL)
        if style_blocks:
            content_html = f'<style>{"".join(style_blocks)}</style>\n{content_html}'
        page_html = build_page(manifest, section, content_html, prev_section, next_section)
        (SITE_DIR / f"{section['slug']}.html").write_text(page_html)
    else:
        content_html = md_to_html(source_text)
        page_html = build_page(manifest, section, content_html, prev_section, next_section)
        (SITE_DIR / f"{section['slug']}.html").write_text(page_html)

    section['last_updated'] = datetime.now().strftime('%Y-%m-%d')

    # Also rebuild index (nav might change)
    index_html = build_index(manifest)
    (SITE_DIR / "index.html").write_text(index_html)

    save_manifest(manifest)
    print(f"  ✓ Updated: {section['slug']}.html ({section['name']})")
    return manifest


def add_section(manifest, name, source_path):
    """Add a new section to the manifest."""
    slug = name.lower().replace(' ', '-').replace("'", '')
    max_order = max((s['order'] for s in manifest['sections']), default=0)

    new_section = {
        "order": max_order + 1,
        "name": name,
        "slug": slug,
        "source": source_path,
        "description": "",
        "audience": "general",
        "last_updated": None
    }

    manifest['sections'].append(new_section)
    save_manifest(manifest)
    print(f"  ✓ Added section: {name} (order {max_order + 1})")
    print(f"    Source: {source_path}")
    print(f"    Run 'rebuild' to generate the page")
    return manifest


def remove_section(manifest, slug):
    """Remove a section from the manifest."""
    before = len(manifest['sections'])
    manifest['sections'] = [s for s in manifest['sections'] if s['slug'] != slug]
    after = len(manifest['sections'])

    if before == after:
        print(f"  ✗ Section '{slug}' not found")
    else:
        save_manifest(manifest)
        # Remove the HTML file if it exists
        html_file = SITE_DIR / f"{slug}.html"
        if html_file.exists():
            html_file.unlink()
        print(f"  ✓ Removed section: {slug}")
        print(f"    Run 'rebuild' to update navigation")
    return manifest


def main():
    parser = argparse.ArgumentParser(description='War Chest Site Builder')
    parser.add_argument('command', choices=['rebuild', 'update', 'add', 'remove', 'investor'],
                       help='Command to execute')
    parser.add_argument('--section', help='Section slug (for update/remove)')
    parser.add_argument('--name', help='Section name (for add)')
    parser.add_argument('--source', help='Source .md path (for add)')

    args = parser.parse_args()
    manifest = load_manifest()

    if args.command == 'rebuild':
        rebuild(manifest)
    elif args.command == 'investor':
        build_investor(manifest)
    elif args.command == 'update':
        if not args.section:
            print("  ✗ --section required for update")
            sys.exit(1)
        update_section(manifest, args.section)
    elif args.command == 'add':
        if not args.name or not args.source:
            print("  ✗ --name and --source required for add")
            sys.exit(1)
        add_section(manifest, args.name, args.source)
    elif args.command == 'remove':
        if not args.section:
            print("  ✗ --section required for remove")
            sys.exit(1)
        remove_section(manifest, args.section)


if __name__ == '__main__':
    main()
