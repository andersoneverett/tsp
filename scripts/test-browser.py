#!/usr/bin/env python3
"""Optional browser smoke test. Requires Playwright, Chromium, and optionally axe-core."""
import argparse
import functools
import json
import re
import shutil
import tempfile
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
import yaml
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--chromium', default=shutil.which('chromium'))
parser.add_argument('--axe', type=Path)
args = parser.parse_args()
prefix = urlsplit(yaml.safe_load((ROOT / '_quarto.yml').read_text())['website']['site-url']).path.strip('/')

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass

with tempfile.TemporaryDirectory(prefix='tsp-browser-') as temporary:
    mount = Path(temporary) / prefix
    mount.parent.mkdir(parents=True, exist_ok=True)
    mount.symlink_to(ROOT / '_site', target_is_directory=True)
    handler = functools.partial(QuietHandler, directory=temporary)
    server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}/{prefix}/'
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=args.chromium, headless=True, args=['--no-sandbox'])
            page = browser.new_page(viewport={'width': 1440, 'height': 1000})
            failures, accessibility = [], []
            def audit(path, viewport):
                if not args.axe:
                    return
                page.add_script_tag(path=str(args.axe))
                result = page.evaluate('''async () => await axe.run(document, {
                  runOnly: {type: 'tag', values: ['wcag2a','wcag2aa','wcag21a','wcag21aa']}
                })''')
                for v in result['violations']:
                    accessibility.append({'page': path, 'viewport': viewport, 'id': v['id'], 'impact': v['impact'],
                                          'nodes': [n['target'] for n in v['nodes']]})
            page.on('pageerror', lambda e: failures.append(str(e)))
            page.on('response', lambda r: failures.append(f'{r.status} {r.url}') if r.status >= 400 else None)
            public_pages = sorted(p.relative_to(ROOT / '_site').as_posix() for p in (ROOT / '_site').rglob('*.html')
                                  if p.relative_to(ROOT / '_site').parts[0] not in ('site_libs', 'assets'))
            for path in public_pages:
                page.goto(base + path, wait_until='networkidle')
                expect(page.locator('main')).to_be_visible()
                assert not page.evaluate('document.documentElement.scrollWidth > innerWidth'), f'Desktop overflow: {path}'
                audit(path, 'desktop')
            Path('/tmp/tsp-accessibility.json').write_text(json.dumps(accessibility, indent=2))
            page.goto(base, wait_until='networkidle')
            page.keyboard.press('Tab')
            expect(page.locator('.skip-link')).to_be_focused()
            page.locator('#quarto-search button').click()
            page.locator('input[type="search"]').fill('compensation')
            result = page.get_by_role('option').filter(has_text=re.compile('national service', re.I)).first
            expect(result).to_be_visible()
            page.keyboard.press('Escape')
            page.goto(base + 'research/', wait_until='networkidle')
            listing = page.locator('#listing-publications .list')
            archive_filter = page.get_by_placeholder('Filter')
            archive_filter.press_sequentially('zz_no_matching_publication')
            expect(listing.locator('.quarto-post:visible')).to_have_count(0)
            expect(page.locator('.listing-no-matching')).to_be_visible()
            archive_filter.fill('')
            archive_filter.press_sequentially('Paid national service')
            expect(listing.locator('.quarto-post:visible')).to_have_count(1)
            category = page.get_by_role('button', name=re.compile('^National service'))
            category.press('Enter')
            expect(category).to_have_attribute('aria-pressed', 'true')
            # Public defaults must show no invented or unconfigured account links.
            page.goto(base + 'get-involved.html', wait_until='networkidle')
            expect(page.locator('[data-social-links] a')).to_have_count(0)
            expect(page.locator('[data-social-unconfigured]')).to_be_visible()
            # Test configuration without modifying real public configuration.
            page.route('**/assets/site-config.json', lambda route: route.fulfill(
                content_type='application/json', body=json.dumps({'socialLinks': {'Test channel': 'https://example.org/tsp', 'Unset': None}})))
            page.reload(wait_until='networkidle')
            expect(page.locator('[data-social-links] a')).to_have_count(1)
            expect(page.locator('[data-social-unconfigured]')).to_be_hidden()
            page.unroute('**/assets/site-config.json')
            page.set_viewport_size({'width': 390, 'height': 844})
            for path in public_pages:
                page.goto(base + path, wait_until='networkidle')
                assert not page.evaluate('document.documentElement.scrollWidth > innerWidth'), f'Mobile overflow: {path}'
                audit(path, 'mobile')
            Path('/tmp/tsp-accessibility.json').write_text(json.dumps(accessibility, indent=2))
            page.goto(base, wait_until='networkidle')
            page.get_by_role('button', name='Toggle navigation').click()
            menu = page.locator('#navbarCollapse')
            expect(menu).to_be_visible()
            menu.get_by_role('link', name='Programs', exact=True).click()
            expect(page).to_have_url(re.compile(re.escape(base) + r'programs/(index.html)?$'))
            page.goto(base, wait_until='networkidle')
            page.screenshot(path='/tmp/tsp-mobile.png', full_page=True)
            if accessibility:
                raise AssertionError('Accessibility violations: ' + json.dumps(accessibility, indent=2))
            assert not failures, 'Browser errors: ' + json.dumps(failures)
            print(f'Passed: {len(public_pages)} pages at desktop and mobile widths; search, filters, keyboard skip link, mobile menu, and optional social configuration.')
            if args.axe:
                print(f'No automated WCAG A/AA violations found on {len(public_pages)} pages. This is not a full accessibility audit.')
            browser.close()
    finally:
        server.shutdown()
