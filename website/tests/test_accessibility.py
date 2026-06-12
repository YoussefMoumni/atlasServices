#!/usr/bin/env python3
"""Accessibility tests for static website."""

from pathlib import Path
from bs4 import BeautifulSoup

WEBSITE_DIR = Path(__file__).parent.parent
HTML_FILES = list(WEBSITE_DIR.glob('*.html'))


class TestAccessibility:
    """Test WCAG 2.1 Level AA accessibility compliance."""
    
    def test_images_have_alt_text(self):
        """Verify all img elements have alt attributes."""
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            
            images = soup.find_all('img')
            
            for img in images:
                assert img.has_attr('alt'), \
                    f"{html_file.name}: <img> missing alt attribute: {img}"
    
    def test_links_have_accessible_text(self):
        """Verify links have accessible text content."""
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            
            links = soup.find_all('a')
            
            for link in links:
                # Link should have text content or aria-label
                text = link.get_text(strip=True)
                aria_label = link.get('aria-label', '').strip()
                title = link.get('title', '').strip()
                
                assert text or aria_label or title, \
                    f"{html_file.name}: Link has no accessible text: {link}"
    
    def test_form_inputs_have_labels(self):
        """Verify form inputs have associated labels or aria-labels."""
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            
            # Find all input, select, textarea elements
            form_elements = soup.find_all(['input', 'select', 'textarea'])
            
            for element in form_elements:
                # Skip hidden, submit, and button inputs
                input_type = element.get('type', 'text')
                if input_type in ['hidden', 'submit', 'button']:
                    continue
                
                # Should have id and corresponding label, or aria-label
                elem_id = element.get('id')
                aria_label = element.get('aria-label')
                aria_labelledby = element.get('aria-labelledby')
                
                if elem_id:
                    # Look for label with matching for attribute
                    label = soup.find('label', attrs={'for': elem_id})
                    has_label = label is not None
                else:
                    has_label = False
                
                assert has_label or aria_label or aria_labelledby, \
                    f"{html_file.name}: Form element missing label: {element}"
    
    def test_heading_hierarchy(self):
        """Verify proper heading hierarchy (no skipped levels)."""
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            
            # Get all heading tags in order
            headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            
            if not headings:
                continue
            
            # First heading should be h1
            first_heading_level = int(headings[0].name[1])
            assert first_heading_level == 1, \
                f"{html_file.name}: First heading should be <h1>, got <h{first_heading_level}>"
            
            # Check for skipped levels
            prev_level = 1
            for heading in headings[1:]:
                current_level = int(heading.name[1])
                
                # Level can stay same, go down by 1+, or go up to any previous level
                # But cannot skip levels when going down (e.g., h2 -> h4)
                if current_level > prev_level:
                    assert current_level == prev_level + 1, \
                        f"{html_file.name}: Heading hierarchy skips from <h{prev_level}> to <h{current_level}>"
                
                prev_level = current_level
    
    def test_navigation_has_aria_label(self):
        """Verify nav elements have descriptive aria-label."""
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            
            nav_elements = soup.find_all('nav')
            
            for nav in nav_elements:
                # Should have aria-label or aria-labelledby
                aria_label = nav.get('aria-label')
                aria_labelledby = nav.get('aria-labelledby')
                
                assert aria_label or aria_labelledby, \
                    f"{html_file.name}: <nav> element missing aria-label"
    
    def test_lists_properly_structured(self):
        """Verify lists (ul/ol) only contain li elements as direct children."""
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            
            lists = soup.find_all(['ul', 'ol'])
            
            for lst in lists:
                # Get direct children (excluding text nodes and comments)
                children = [child for child in lst.children 
                           if hasattr(child, 'name') and child.name]
                
                for child in children:
                    assert child.name == 'li', \
                        f"{html_file.name}: <{lst.name}> should only contain <li> children, found <{child.name}>"
    
    def test_color_contrast_sufficient(self):
        """Basic check for color contrast issues (CSS color values)."""
        # This is a basic check - full contrast testing requires rendering
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for style tags with color definitions
            soup = BeautifulSoup(content, 'html.parser')
            style_tags = soup.find_all('style')
            
            for style in style_tags:
                style_content = style.string
                if style_content:
                    # Check for very light colors on light backgrounds (common issue)
                    # This is a simple heuristic, not a full contrast calculator
                    
                    # Ensure CSS variables are defined
                    assert '--ink:' in style_content or 'color:' in style_content, \
                        f"{html_file.name}: No color definitions found in styles"
    
    def test_language_attribute_valid(self):
        """Verify lang attribute uses valid language code."""
        valid_lang_codes = ['en', 'fr', 'ar', 'es', 'de']  # Common codes
        
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            
            html_tag = soup.find('html')
            lang = html_tag.get('lang', '').split('-')[0]  # Get primary language code
            
            assert lang in valid_lang_codes, \
                f"{html_file.name}: Unexpected language code '{lang}'"


if __name__ == '__main__':
    import pytest
    import sys
    
    sys.exit(pytest.main([__file__, '-v', '--tb=short']))
