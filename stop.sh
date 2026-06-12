#!/usr/bin/env bash
set -e

# Atlas Maroc Capital Markets - Static Website Stop Script

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$PROJECT_ROOT/.pids"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo_info() { echo -e "${BLUE}ℹ${NC} $1"; }
echo_success() { echo -e "${GREEN}✓${NC} $1"; }
echo_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
echo_error() { echo -e "${RED}✗${NC} $1"; }

stop_server() {
    if [ ! -f "$PID_FILE" ]; then
        echo_warning "No running server found (no PID file)"
        return 0
    fi

    local pid=$(cat "$PID_FILE")

    if ps -p $pid > /dev/null 2>&1; then
        echo_info "Stopping server (PID: $pid)..."
        kill $pid 2>/dev/null || true

        # Wait for process to stop
        local count=0
        while ps -p $pid > /dev/null 2>&1 && [ $count -lt 10 ]; do
            sleep 0.5
            count=$((count + 1))
        done

        if ps -p $pid > /dev/null 2>&1; then
            echo_warning "Process did not stop gracefully, forcing..."
            kill -9 $pid 2>/dev/null || true
        fi

        echo_success "Server stopped"
    else
        echo_warning "Server not running (stale PID file)"
    fi

    rm -f "$PID_FILE"
}

main() {
    stop_server
    echo_success "All services stopped"
}

main "$@"
