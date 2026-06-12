#!/usr/bin/env python3
"""HTML validation tests for static website."""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import html5lib

# Get all HTML files in the website directory
WEBSITE_DIR = Path(__file__).parent.parent
HTML_FILES = list(WEBSITE_DIR.glob('*.html'))

class TestHTMLValidation:
    """Test HTML structure and validity."""
    
    def test_html_files_exist(self):
        """Verify all expected HTML files exist."""
        expected_files = [
            'index.html',
            'advisory.html',
            'brokerage.html',
            'asset-management.html',
            'research.html',
            'capital-raising.html',
            'trading.html'
        ]
        
        existing_files = [f.name for f in HTML_FILES]
        
        for expected in expected_files:
            assert expected in existing_files, f"Missing file: {expected}"
    
    def test_html5_validity(self):
        """Parse each HTML file with html5lib to check validity."""
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # html5lib will raise errors for invalid HTML
            try:
                doc = html5lib.parse(content, namespaceHTMLElements=False)
                assert doc is not None, f"{html_file.name}: Failed to parse"
            except Exception as e:
                raise AssertionError(f"{html_file.name}: HTML5 parsing error: {e}")
    
    def test_doctype_present(self):
        """Verify DOCTYPE declaration is present."""
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            assert '<!DOCTYPE html>' in content or '<!doctype html>' in content, \
                f"{html_file.name}: Missing DOCTYPE declaration"
    
    def test_html_lang_attribute(self):
        """Verify html tag has lang attribute."""
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            
            html_tag = soup.find('html')
            assert html_tag is not None, f"{html_file.name}: No <html> tag"
            assert html_tag.get('lang'), f"{html_file.name}: Missing lang attribute on <html>"
    
    def test_charset_meta_present(self):
        """Verify charset meta tag is present."""
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            
            charset_meta = soup.find('meta', charset=True)
            assert charset_meta is not None, f"{html_file.name}: Missing charset meta tag"
            assert charset_meta.get('charset').lower() == 'utf-8', \
                f"{html_file.name}: Charset should be UTF-8"
    
    def test_viewport_meta_present(self):
        """Verify viewport meta tag is present for responsive design."""
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            
            viewport = soup.find('meta', attrs={'name': 'viewport'})
            assert viewport is not None, f"{html_file.name}: Missing viewport meta tag"
            
            content = viewport.get('content', '')
            assert 'width=device-width' in content, \
                f"{html_file.name}: Viewport should include width=device-width"
    
    def test_title_present(self):
        """Verify title tag is present and not empty."""
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            
            title = soup.find('title')
            assert title is not None, f"{html_file.name}: Missing <title> tag"
            assert title.string and title.string.strip(), \
                f"{html_file.name}: <title> tag is empty"
    
    def test_single_h1_per_page(self):
        """Verify each page has exactly one h1 heading."""
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            
            h1_tags = soup.find_all('h1')
            assert len(h1_tags) == 1, \
                f"{html_file.name}: Should have exactly 1 <h1>, found {len(h1_tags)}"
            
            assert h1_tags[0].string and h1_tags[0].string.strip(), \
                f"{html_file.name}: <h1> should not be empty"
    
    def test_no_empty_links(self):
        """Verify no links have empty href attributes."""
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            
            links = soup.find_all('a', href=True)
            for link in links:
                href = link.get('href', '').strip()
                assert href, f"{html_file.name}: Found <a> tag with empty href"
    
    def test_semantic_html5_structure(self):
        """Verify proper use of semantic HTML5 elements."""
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            
            # Should have header, main, footer
            assert soup.find('header'), f"{html_file.name}: Missing <header> element"
            assert soup.find('main'), f"{html_file.name}: Missing <main> element"
            assert soup.find('footer'), f"{html_file.name}: Missing <footer> element"


class TestContentStructure:
    """Test content structure and consistency."""
    
    def test_navigation_present(self):
        """Verify navigation is present on all pages."""
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            
            nav = soup.find('nav')
            assert nav is not None, f"{html_file.name}: Missing <nav> element"
    
    def test_brand_logo_present(self):
        """Verify brand logo/link is present."""
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            
            brand = soup.find('a', class_='brand')
            assert brand is not None, f"{html_file.name}: Missing brand link"
            
            brand_text = brand.get_text()
            assert 'Atlas Maroc' in brand_text, f"{html_file.name}: Brand should contain 'Atlas Maroc'"
    
    def test_consistent_navigation_links(self):
        """Verify navigation links are consistent across pages."""
        expected_links = [
            'index.html',
            'advisory.html',
            'brokerage.html',
            'asset-management.html',
            'research.html',
            'capital-raising.html',
            'trading.html'
        ]
        
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            
            nav = soup.find('nav')
            nav_links = [a.get('href') for a in nav.find_all('a', href=True)]
            
            for expected in expected_links:
                assert expected in nav_links, \
                    f"{html_file.name}: Navigation missing link to {expected}"


if __name__ == '__main__':
    import pytest
    import sys
    
    # Run tests with verbose output
    sys.exit(pytest.main([__file__, '-v', '--tb=short']))
