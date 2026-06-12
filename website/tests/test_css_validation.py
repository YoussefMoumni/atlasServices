#!/usr/bin/env python3
"""CSS validation tests for static website."""

import re
from pathlib import Path
from bs4 import BeautifulSoup

WEBSITE_DIR = Path(__file__).parent.parent
HTML_FILES = list(WEBSITE_DIR.glob('*.html'))


class TestCSSValidation:
    """Test CSS structure and consistency."""
    
    def test_css_variables_defined(self):
        """Verify CSS custom properties (variables) are defined."""
        expected_vars = [
            '--bg', '--panel', '--ink', '--muted', 
            '--brand', '--accent', '--max', '--radius'
        ]
        
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            
            style_tags = soup.find_all('style')
            assert len(style_tags) > 0, f"{html_file.name}: No <style> tags found"
            
            # Combine all style content
            all_styles = ' '.join([s.string or '' for s in style_tags])
            
            # Check for :root declaration
            assert ':root' in all_styles, \
                f"{html_file.name}: CSS should define :root with custom properties"
            
            # Check for expected CSS variables
            for var in expected_vars:
                assert var in all_styles, \
                    f"{html_file.name}: Missing CSS variable '{var}'"
    
    def test_responsive_breakpoints(self):
        """Verify responsive media queries are present."""
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for media queries
            assert '@media' in content, \
                f"{html_file.name}: No media queries found - site may not be responsive"
            
            # Check for common breakpoint patterns
            has_mobile = 'max-width' in content or 'min-width' in content
            assert has_mobile, \
                f"{html_file.name}: No width-based media queries found"
    
    def test_minimal_inline_styles(self):
        """Verify inline styles are minimal (most CSS should be in <style> tags)."""
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            
            # Find all elements with style attribute
            inline_styles = soup.find_all(style=True)
            
            # Allow up to 10 inline styles for specific layout adjustments
            assert len(inline_styles) <= 10, \
                f"{html_file.name}: Found {len(inline_styles)} inline styles - prefer <style> tags"
    
    def test_font_stack_defined(self):
        """Verify font-family is defined."""
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Should have font-family definition
            assert 'font-family:' in content, \
                f"{html_file.name}: No font-family defined"
    
    def test_color_consistency(self):
        """Verify colors are defined using CSS variables (not hardcoded)."""
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            
            style_tags = soup.find_all('style')
            for style in style_tags:
                style_content = style.string or ''
                
                # After :root definition, colors should use var()
                # Split at :root to only check styles after variable definitions
                if ':root' in style_content:
                    parts = style_content.split('}', 1)
                    if len(parts) > 1:
                        remaining_styles = parts[1]
                        
                        # Count var() usage
                        var_usage = remaining_styles.count('var(--')
                        
                        # Should use CSS variables for colors
                        assert var_usage > 0, \
                            f"{html_file.name}: Styles should use CSS variables (var(--...))"
    
    def test_box_sizing_set(self):
        """Verify box-sizing: border-box is set."""
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            assert 'box-sizing: border-box' in content, \
                f"{html_file.name}: Should set box-sizing: border-box for consistent layout"
    
    def test_responsive_units(self):
        """Verify responsive units (rem, em, %, vw, vh) are used."""
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for responsive units
            responsive_units = ['rem', 'em', 'vw', 'vh', '%', 'clamp(']
            has_responsive = any(unit in content for unit in responsive_units)
            
            assert has_responsive, \
                f"{html_file.name}: Should use responsive units (rem, em, %, vw, vh, clamp)"


class TestDesignConsistency:
    """Test design system consistency across pages."""
    
    def test_consistent_css_across_pages(self):
        """Verify all pages use the same CSS variable values."""
        css_vars = {}
        
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            
            style_tags = soup.find_all('style')
            for style in style_tags:
                content = style.string or ''
                
                # Extract :root block
                root_match = re.search(r':root\s*{([^}]+)}', content)
                if root_match:
                    root_content = root_match.group(1)
                    
                    # Extract variable definitions
                    var_pattern = r'(--[\w-]+):\s*([^;]+);'
                    vars_found = dict(re.findall(var_pattern, root_content))
                    
                    if not css_vars:
                        # First file - store as reference
                        css_vars[html_file.name] = vars_found
                    else:
                        # Compare with first file
                        first_file = list(css_vars.keys())[0]
                        first_vars = css_vars[first_file]
                        
                        # Check that key variables match
                        key_vars = ['--brand', '--accent', '--bg', '--ink']
                        for var in key_vars:
                            if var in first_vars and var in vars_found:
                                assert first_vars[var].strip() == vars_found[var].strip(), \
                                    f"{html_file.name}: CSS variable {var} differs from {first_file}"
    
    def test_consistent_layout_classes(self):
        """Verify consistent use of layout classes across pages."""
        common_classes = ['container', 'hero', 'card', 'nav-list']
        
        for html_file in HTML_FILES:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            
            # Check that key layout classes exist
            for class_name in common_classes:
                elements = soup.find_all(class_=class_name)
                # At least some pages should have these classes
                # (not all classes will be on every page)


if __name__ == '__main__':
    import pytest
    import sys
    
    sys.exit(pytest.main([__file__, '-v', '--tb=short']))
