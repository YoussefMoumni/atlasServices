#!/usr/bin/env bash
set -e

# Atlas Maroc Capital Markets - Static Website Start Script

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WEBSITE_DIR="$PROJECT_ROOT/website"
PID_FILE="$PROJECT_ROOT/.pids"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo_info() { echo -e "${BLUE}ℹ${NC} $1"; }
echo_success() { echo -e "${GREEN}✓${NC} $1"; }
echo_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
echo_error() { echo -e "${RED}✗${NC} $1"; }

# Find available port
find_available_port() {
    local start_port=$1
    local port=$start_port
    while lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; do
        port=$((port + 1))
    done
    echo $port
}

# Check prerequisites
check_prerequisites() {
    echo_info "Checking prerequisites..."

    if command -v python3 >/dev/null 2>&1; then
        echo_success "Python 3 found: $(python3 --version)"
        return 0
    fi

    if command -v python >/dev/null 2>&1; then
        echo_success "Python found: $(python --version)"
        return 0
    fi

    echo_error "Python is not installed. Please install Python 3."
    echo_info "Visit: https://www.python.org/downloads/"
    exit 1
}

# Start the static server
start_server() {
    echo_info "Starting Atlas Maroc Capital Markets static website..."

    cd "$WEBSITE_DIR"

    # Find available port
    local port=$(find_available_port 8000)

    # Start Python HTTP server
    if command -v python3 >/dev/null 2>&1; then
        python3 -m http.server $port > /dev/null 2>&1 &
    else
        python -m http.server $port > /dev/null 2>&1 &
    fi

    local server_pid=$!
    echo "$server_pid" > "$PID_FILE"

    # Wait for server to start
    sleep 1

    if ps -p $server_pid > /dev/null; then
        echo_success "Static website server started on port $port (PID: $server_pid)"
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo -e "${GREEN}Atlas Maroc Capital Markets${NC}"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo -e "  ${BLUE}Website URL:${NC}  http://localhost:$port"
        echo ""
        echo -e "${YELLOW}Available Pages:${NC}"
        echo "  • Overview:          http://localhost:$port/"
        echo "  • Advisory:          http://localhost:$port/advisory.html"
        echo "  • Brokerage:         http://localhost:$port/brokerage.html"
        echo "  • Asset Management:  http://localhost:$port/asset-management.html"
        echo "  • Research:          http://localhost:$port/research.html"
        echo "  • Capital Raising:   http://localhost:$port/capital-raising.html"
        echo "  • Trading:           http://localhost:$port/trading.html"
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo -e "${BLUE}Commands:${NC}"
        echo "  • Stop server:  ./stop.sh"
        echo ""
    else
        echo_error "Failed to start server"
        rm -f "$PID_FILE"
        exit 1
    fi
}

# Main execution
main() {
    check_prerequisites

    # Check if already running
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if ps -p $pid > /dev/null 2>&1; then
            echo_warning "Server is already running (PID: $pid)"
            echo_info "Use ./stop.sh to stop it first"
            exit 0
        else
            echo_warning "Stale PID file found, removing..."
            rm -f "$PID_FILE"
        fi
    fi

    start_server
}

main "$@"
