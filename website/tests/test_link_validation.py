#!/usr/bin/env python3
"""Link validation tests for static website."""

from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

WEBSITE_DIR = Path(__file__).parent.parent
HTML_FILES = list(WEBSITE_DIR.glob('*.html'))


class TestLinkValidation:
    """Test internal and external link integrity."""
    
    def test_internal_links_valid(self):
        """Verify all internal links point to existing files."""
        existing_files = {f.name for f in HTML_FILES}
        
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            
            links = soup.find_all('a', href=True)
            
            for link in links:
                href = link.get('href', '')
                
                # Skip external links, anchors, and special protocols
                if (href.startswith('http://') or 
                    href.startswith('https://') or 
                    href.startswith('mailto:') or
                    href.startswith('tel:') or
                    href.startswith('#')):
                    continue
                
                # Extract filename from href (remove hash fragments)
                target_file = href.split('#')[0]
                
                if target_file:  # Not a pure anchor link
                    assert target_file in existing_files, \
                        f"{html_file.name}: Broken link to '{href}' - file not found"
    
    def test_no_duplicate_ids(self):
        """Verify no duplicate IDs exist within each page."""
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            
            # Find all elements with id attribute
            elements_with_id = soup.find_all(id=True)
            ids = [elem.get('id') for elem in elements_with_id]
            
            # Check for duplicates
            unique_ids = set(ids)
            assert len(ids) == len(unique_ids), \
                f"{html_file.name}: Found duplicate IDs: {[i for i in ids if ids.count(i) > 1]}"
    
    def test_anchor_links_valid(self):
        """Verify anchor links (#id) point to existing IDs on the page."""
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            
            # Get all IDs on the page
            page_ids = {elem.get('id') for elem in soup.find_all(id=True)}
            
            # Get all anchor links
            anchor_links = soup.find_all('a', href=lambda x: x and x.startswith('#'))
            
            for link in anchor_links:
                href = link.get('href')
                target_id = href[1:]  # Remove the #
                
                if target_id:  # Not just a bare #
                    assert target_id in page_ids, \
                        f"{html_file.name}: Anchor link '{href}' points to non-existent ID"
    
    def test_cross_page_references(self):
        """Verify links between service pages work correctly."""
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            
            # Find all internal page links
            internal_links = soup.find_all('a', href=lambda x: 
                x and x.endswith('.html') and not x.startswith('http'))
            
            for link in internal_links:
                href = link.get('href')
                target_file = WEBSITE_DIR / href.split('#')[0]
                
                assert target_file.exists(), \
                    f"{html_file.name}: Link to '{href}' points to non-existent file"


class TestNavigationConsistency:
    """Test navigation consistency across all pages."""
    
    def test_all_service_pages_linked_from_index(self):
        """Verify index.html links to all service pages."""
        service_pages = [
            'advisory.html',
            'brokerage.html',
            'asset-management.html',
            'research.html',
            'capital-raising.html',
            'trading.html'
        ]
        
        index_file = WEBSITE_DIR / 'index.html'
        with open(index_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        
        for service in service_pages:
            assert service in links, f"index.html: Missing link to {service}"
    
    def test_brand_logo_links_to_home(self):
        """Verify brand logo links back to index.html."""
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            
            brand = soup.find('a', class_='brand')
            assert brand is not None, f"{html_file.name}: Missing brand link"
            
            href = brand.get('href')
            assert href in ['index.html', '/'], \
                f"{html_file.name}: Brand link should point to index.html or /, got '{href}'"


if __name__ == '__main__':
    import pytest
    import sys
    
    sys.exit(pytest.main([__file__, '-v', '--tb=short']))
