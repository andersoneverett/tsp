#!/usr/bin/env python3
"""Validate public metadata, workflow structure, built links, and publication boundaries."""
import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import yaml

ROOT = Path(__file__).resolve().parents[1]
errors = []

def require(condition, message):
    if not condition:
        errors.append(message)

def metadata(path):
    text = path.read_text()
    require(text.startswith('---\n'), f'{path.relative_to(ROOT)}: missing metadata block')
    try:
        return yaml.safe_load(text.split('---', 2)[1]) or {}
    except (yaml.YAMLError, IndexError) as exc:
        errors.append(f'{path}: invalid YAML: {exc}')
        return {}

def source_checks():
    config = yaml.safe_load((ROOT / '_quarto.yml').read_text())
    require(config['project']['type'] == 'website', 'Expected a Quarto website')
    require(config['execute']['enabled'] is False, 'Public website must not execute research')
    require(config['website']['draft-mode'] == 'gone', 'Draft content must remain unpublished')
    for pattern in config['project']['render']:
        require(not pattern.startswith(('drafts', 'templates', 'research-projects', '**')), f'Unsafe public render pattern: {pattern}')
    site_url = config['website']['site-url']
    require(site_url.startswith('https://') and site_url.endswith('/'), 'site-url must be HTTPS with a trailing slash')
    for path in [*ROOT.glob('*.qmd'), *ROOT.glob('programs/**/*.qmd'), *ROOT.glob('news/**/*.qmd'), *ROOT.glob('research/**/*.qmd')]:
        meta = metadata(path)
        if meta.get('draft'):
            continue
        require(bool(meta.get('title') or meta.get('pagetitle')), f'{path}: title required')
        if path.name == 'index.qmd' and ('posts' in path.parts or 'publications' in path.parts):
            for field in ('description', 'summary', 'date', 'author', 'categories'):
                require(bool(meta.get(field)), f'{path.relative_to(ROOT)}: {field} required')
            require('REPLACE:' not in path.read_text(), f'{path}: unfinished template in public content')
        require(not meta.get('execute', {}).get('enabled', False) if isinstance(meta.get('execute', {}), dict) else True,
                f'{path}: research execution belongs outside the website')
    social = json.loads((ROOT / 'assets/site-config.json').read_text())
    for label, url in social['socialLinks'].items():
        require(url is None or (isinstance(url, str) and url.startswith('https://') and bool(urlsplit(url).hostname)),
                f'{label}: social URL must be null or an HTTPS address')
    for path in ROOT.glob('templates/*.qmd'):
        require(metadata(path).get('draft') is True, f'{path}: templates must default to draft')
    for path in ROOT.glob('.github/workflows/*.yml'):
        # BaseLoader preserves the Actions keyword "on" under YAML 1.1 parsers.
        workflow = yaml.load(path.read_text(), Loader=yaml.BaseLoader)
        require(all(k in workflow for k in ('name', 'on', 'jobs')), f'{path}: invalid Actions structure')
        require('workflow_dispatch' in workflow['on'], f'{path}: manual retry trigger missing')
    lock = json.loads((ROOT / 'renv.lock').read_text())
    require(all(p in lock['Packages'] for p in ('renv', 'knitr', 'rmarkdown')), 'R report dependencies missing from lockfile')

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.links, self.ids, self.images, self.h1 = [], set(), [], 0
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        if tag == 'h1':
            self.h1 += 1
        if tag == 'img':
            self.images.append(attrs)
        for attr in ('href', 'src'):
            if attrs.get(attr):
                self.links.append(attrs[attr])

def built_checks():
    site = ROOT / '_site'
    require((site / 'index.html').exists(), 'Render the website before built checks')
    pages = {p.resolve(): Page(p.read_text()) for p in site.rglob('*.html') if 'site_libs' not in p.parts}
    prefix = urlsplit(yaml.safe_load((ROOT / '_quarto.yml').read_text())['website']['site-url']).path.rstrip('/')
    checked = 0
    for path, page in pages.items():
        require(page.h1 == 1, f'{path.relative_to(site)}: expected one main heading, found {page.h1}')
        for img in page.images:
            require('alt' in img, f'{path.relative_to(site)}: image has no alternative text: {img.get("src")}')
        require(':::' not in path.read_text(), f'{path.relative_to(site)}: unparsed fenced layout markup')
        for link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc or link.startswith(('data:', 'javascript:')):
                continue
            raw = unquote(url.path)
            if raw.startswith('/'):
                if prefix and (raw == prefix or raw.startswith(prefix + '/')):
                    raw = raw[len(prefix):]
                target = site / raw.lstrip('/')
            else:
                target = path.parent / raw if raw else path
            if target.is_dir():
                target /= 'index.html'
            target = target.resolve()
            require(target.is_relative_to(site.resolve()), f'{path}: link escapes generated site: {link}')
            require(target.exists(), f'{path.relative_to(site)}: missing target {link}')
            if url.fragment and target in pages:
                require(unquote(url.fragment) in pages[target].ids,
                        f'{path.relative_to(site)}: missing anchor {link}')
            checked += 1
    for private in ('drafts', 'templates', 'research-projects', 'renv', '.github', 'scripts'):
        require(not (site / private).exists(), f'Unpublished directory exposed: {private}')
    for feed in ('news/index.xml', 'research/index.xml'):
        require((site / feed).exists(), f'Missing RSS feed: {feed}')
    require((site / 'search.json').exists(), 'Search index missing')
    print(f'Checked {len(pages)} public HTML pages and {checked} internal links/assets.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-only', action='store_true')
    args = parser.parse_args()
    try:
        source_checks()
        if not args.source_only:
            built_checks()
    except (OSError, ValueError, KeyError, yaml.YAMLError) as exc:
        errors.append(str(exc))
    if errors:
        print('\n'.join(f'ERROR: {e}' for e in errors), file=sys.stderr)
        sys.exit(1)
    print('Validation passed.')
