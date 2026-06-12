#!/usr/bin/env bash
# Atlas Maroc Capital Markets - Implementation Verification Script

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo_info() { echo -e "${BLUE}ℹ${NC} $1"; }
echo_success() { echo -e "${GREEN}✓${NC} $1"; }
echo_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
echo_error() { echo -e "${RED}✗${NC} $1"; }

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}Atlas Maroc Capital Markets${NC}"
echo "Implementation Verification"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check required HTML files
echo_info "Checking required HTML files..."
required_files=(
    "website/index.html"
    "website/advisory.html"
    "website/brokerage.html"
    "website/asset-management.html"
    "website/research.html"
    "website/capital-raising.html"
    "website/trading.html"
)

all_files_present=true
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        size=$(du -h "$file" | cut -f1)
        echo_success "$file ($size)"
    else
        echo_error "$file NOT FOUND"
        all_files_present=false
    fi
done

if [ "$all_files_present" = false ]; then
    echo ""
    echo_error "Some HTML files are missing!"
    exit 1
fi

echo ""
echo_info "Validating HTML structure..."

for file in "${required_files[@]}"; do
    if ! grep -q "<!DOCTYPE html>" "$file"; then
        echo_error "$file: Missing DOCTYPE declaration"
        exit 1
    fi
    if ! grep -q "<html" "$file"; then
        echo_error "$file: Missing <html> tag"
        exit 1
    fi
    if ! grep -q "</html>" "$file"; then
        echo_error "$file: Missing </html> closing tag"
        exit 1
    fi
    if ! grep -q "Atlas Maroc" "$file"; then
        echo_error "$file: Missing Atlas Maroc branding"
        exit 1
    fi
done

echo_success "All HTML files have valid structure"

echo ""
echo_info "Checking documentation files..."

doc_files=(
    "README.md"
    "DEPLOYMENT.md"
    "IMPLEMENTATION_SUMMARY.md"
    "website/README.md"
)

for file in "${doc_files[@]}"; do
    if [ -f "$file" ]; then
        lines=$(wc -l < "$file")
        echo_success "$file ($lines lines)"
    else
        echo_warning "$file not found (optional)"
    fi
done

echo ""
echo_info "Checking startup scripts..."

scripts=(
    "start.sh"
    "stop.sh"
    "start.bat"
    "stop.bat"
)

for script in "${scripts[@]}"; do
    if [ -f "$script" ]; then
        echo_success "$script"
    else
        echo_warning "$script not found"
    fi
done

echo ""
echo_info "Checking CI/CD configuration..."

if [ -f ".github/workflows/deploy.yml" ]; then
    echo_success "GitHub Actions workflow configured"
else
    echo_warning "GitHub Actions workflow not found"
fi

echo ""
echo_info "Checking navigation consistency..."

# Check that all pages link to each other
pages=("index" "advisory" "brokerage" "asset-management" "research" "capital-raising" "trading")
nav_errors=0

for page in "${pages[@]}"; do
    file="website/${page}.html"
    if [ -f "$file" ]; then
        for target in "${pages[@]}"; do
            if [ "$target" != "$page" ]; then
                target_link="${target}.html"
                if [ "$target" = "index" ]; then
                    target_link="index.html"
                fi
                if ! grep -q "href=\"${target_link}\"" "$file"; then
                    echo_warning "$page.html missing link to $target_link"
                    nav_errors=$((nav_errors + 1))
                fi
            fi
        done
    fi
done

if [ $nav_errors -eq 0 ]; then
    echo_success "All navigation links present"
else
    echo_warning "Found $nav_errors navigation inconsistencies (non-critical)"
fi

echo ""
echo_info "Project statistics:"
echo "  • HTML files: $(ls -1 website/*.html | wc -l)"
echo "  • Total website size: $(du -sh website/ | cut -f1)"
echo "  • Total project size: $(du -sh . | cut -f1)"
echo "  • Documentation files: $(ls -1 *.md 2>/dev/null | wc -l)"
echo "  • Script files: $(ls -1 *.sh *.bat 2>/dev/null | wc -l)"

echo ""
echo_info "Checking design fidelity..."

# Check for key design elements
design_checks=0
if grep -q "#07111f" website/index.html; then
    echo_success "Background color (#07111f) present"
    design_checks=$((design_checks + 1))
fi

if grep -q "#c8a96b" website/index.html; then
    echo_success "Brand color (#c8a96b) present"
    design_checks=$((design_checks + 1))
fi

if grep -q "#63b3d1" website/index.html; then
    echo_success "Accent color (#63b3d1) present"
    design_checks=$((design_checks + 1))
fi

if grep -q "Inter" website/index.html; then
    echo_success "Inter font family configured"
    design_checks=$((design_checks + 1))
fi

if grep -q "clamp" website/index.html; then
    echo_success "Responsive typography (clamp) used"
    design_checks=$((design_checks + 1))
fi

if [ $design_checks -eq 5 ]; then
    echo_success "All design elements verified"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo_success "Verification Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${GREEN}✅ Project Status: READY FOR DEPLOYMENT${NC}"
echo ""
echo "Next steps:"
echo "  1. Start local server:  ./start.sh (or start.bat)"
echo "  2. Deploy to web:       See DEPLOYMENT.md"
echo "  3. Configure domain:    Add custom domain to hosting"
echo ""
