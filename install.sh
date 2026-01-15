#!/bin/bash

# HIPE Installation Script
# Installs or uninstalls HIPE file versioning CLI

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_PATH="/usr/local/bin/hipe"
HIPE_SCRIPT="$SCRIPT_DIR/hipe.py"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Check if Python 3 is installed
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3.13 or higher."
        exit 1
    fi
    
    python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    print_info "Found Python $python_version"
}

# Install HIPE
install() {
    print_info "Installing HIPE..."
    
    check_python
    
    if [ ! -f "$HIPE_SCRIPT" ]; then
        print_error "hipe.py not found in $SCRIPT_DIR"
        exit 1
    fi
    
    # Make hipe.py executable
    chmod +x "$HIPE_SCRIPT"
    
    # Create wrapper script
    sudo tee "$INSTALL_PATH" > /dev/null <<EOF
#!/bin/bash
exec python3 "$HIPE_SCRIPT" "\$@"
EOF
    
    sudo chmod +x "$INSTALL_PATH"
    
    print_success "HIPE installed successfully!"
    print_info "Usage: hipe <command> [options]"
    print_info "Run 'hipe --help' for more information"
}

# Uninstall HIPE
uninstall() {
    print_info "Uninstalling HIPE..."
    
    if [ -f "$INSTALL_PATH" ]; then
        sudo rm "$INSTALL_PATH"
        print_success "HIPE uninstalled successfully!"
    else
        print_error "HIPE is not installed"
        exit 1
    fi
}

# Main logic
if [[ "$1" == "-u" ]] || [[ "$1" == "--uninstall" ]]; then
    uninstall
else
    install
fi
