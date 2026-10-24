#!/usr/bin/env python3
"""Real Quarto integration test for ordinary browser-editor publication paths."""
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
news = ROOT / 'news/posts/zz-listing-smoke'
research = ROOT / 'research/publications/zz-listing-smoke'
draft = ROOT / 'news/posts/zz-draft-smoke'
outside = ROOT / 'drafts/zz-exclusion-smoke.qmd'
created = []

def render():
    subprocess.run(['quarto', 'render'], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)

def article(title, draft_flag=False):
    return f'''---
title: "{title}"
description: "Integration test; removed before final output."
summary: "Temporary publication test."
date: 2026-10-23
author: Teen Service Project
categories: [Validation]
draft: {str(draft_flag).lower()}
---

Temporary integration test content.
'''

try:
    # Refuse to overwrite anything, including material from an interrupted run.
    for path in (news, research, draft, outside):
        if path.exists():
            raise RuntimeError(f'Refusing to replace existing file: {path}')
    for path, title, flag in ((news, 'TSP_NEWS_TEST_SENTINEL', False),
                              (research, 'TSP_RESEARCH_TEST_SENTINEL', False),
                              (draft, 'TSP_UNPUBLISHED_SENTINEL', True)):
        path.mkdir()
        created.append(path)
        (path / 'index.qmd').write_text(article(title, flag))
    outside.write_text(article('TSP_OUTSIDE_SENTINEL'))
    created.append(outside)
    render()
    site = ROOT / '_site'
    for file, sentinel in (
        ('news/index.html', 'TSP_NEWS_TEST_SENTINEL'),
        ('index.html', 'TSP_NEWS_TEST_SENTINEL'),
        ('news/index.xml', 'TSP_NEWS_TEST_SENTINEL'),
        ('research/index.html', 'TSP_RESEARCH_TEST_SENTINEL'),
        ('research/index.xml', 'TSP_RESEARCH_TEST_SENTINEL'),
        ('search.json', 'TSP_RESEARCH_TEST_SENTINEL'),
        ('search.json', 'TSP_NEWS_TEST_SENTINEL')):
        assert sentinel in (site / file).read_text(), f'{sentinel} missing from {file}'
    for path in site.rglob('*'):
        if path.is_file() and path.suffix in ('.html', '.json', '.xml'):
            text = path.read_text()
            assert 'TSP_UNPUBLISHED_SENTINEL' not in text, f'Draft content exposed in {path}'
            assert 'TSP_OUTSIDE_SENTINEL' not in text, f'Excluded content exposed in {path}'
    assert not (site / 'drafts').exists(), 'Draft directory exposed'
    print('Passed: new news and research entries update archives, homepage, RSS, and search; drafts stay unpublished.')
finally:
    for path in created:
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
    # Remove only this test's generated directories; rebuild real listings/indexes.
    for relative in ('news/posts/zz-listing-smoke', 'research/publications/zz-listing-smoke', 'news/posts/zz-draft-smoke'):
        shutil.rmtree(ROOT / '_site' / relative, ignore_errors=True)
    if created:
        render()
