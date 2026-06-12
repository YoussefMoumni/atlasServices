#!/bin/bash
# Comprehensive test runner for Atlas Maroc Capital Markets website

set -e

echo "=================================================="
echo "Atlas Maroc Capital Markets - Test Suite"
echo "=================================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if dependencies are installed
echo "📦 Checking dependencies..."
if ! python3 -c "import bs4, html5lib, pytest" 2>/dev/null; then
    echo -e "${YELLOW}Installing test dependencies...${NC}"
    pip install -q -r requirements-test.txt
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${GREEN}✓ Dependencies already installed${NC}"
fi
echo ""

# Run HTML validation tests
echo "🔍 Running HTML Validation Tests..."
echo "-----------------------------------"
python3 -m pytest tests/test_html_validation.py -v --tb=short
echo ""

# Run link validation tests
echo "🔗 Running Link Validation Tests..."
echo "-----------------------------------"
python3 -m pytest tests/test_link_validation.py -v --tb=short
echo ""

# Run accessibility tests
echo "♿ Running Accessibility Tests..."
echo "-----------------------------------"
python3 -m pytest tests/test_accessibility.py -v --tb=short
echo ""

# Run CSS validation tests
echo "🎨 Running CSS Validation Tests..."
echo "-----------------------------------"
python3 -m pytest tests/test_css_validation.py -v --tb=short
echo ""

# Summary
echo "=================================================="
echo "📊 Test Summary"
echo "=================================================="
python3 -m pytest tests/ --tb=no --no-header -q
echo ""

# Check if all tests passed
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ ALL TESTS PASSED${NC}"
    echo ""
    echo "The website is ready for deployment!"
    echo ""
    echo "To view the website locally, run:"
    echo "  python3 -m http.server 8000"
    echo ""
    echo "Then open: http://localhost:8000"
    echo ""
    echo "Quality report available in: QUALITY_REPORT.md"
    exit 0
else
    echo -e "${RED}❌ SOME TESTS FAILED${NC}"
    echo ""
    echo "Please review the test output above and fix any issues."
    exit 1
fi
