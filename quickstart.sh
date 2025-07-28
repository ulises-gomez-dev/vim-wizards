#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Welcome to VimWizards Setup!${NC}"
echo "=============================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed.${NC}"
    echo "Please install Python 3 and try again."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo -e "${GREEN}Found Python ${PYTHON_VERSION}${NC}"

# Check if pip is installed
if ! python3 -m pip --version &> /dev/null; then
    echo -e "${YELLOW}pip is not installed.${NC}"
    read -p "Would you like to install pip? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Installing pip..."
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        python3 get-pip.py --user
        rm get-pip.py
        
        # Add pip to PATH for current session
        export PATH="$HOME/.local/bin:$PATH"
        
        # Verify pip installation
        if ! python3 -m pip --version &> /dev/null; then
            echo -e "${RED}Failed to install pip. Please install it manually.${NC}"
            exit 1
        fi
        echo -e "${GREEN}pip installed successfully!${NC}"
    else
        echo -e "${RED}pip is required to continue. Exiting.${NC}"
        exit 1
    fi
fi

# Check if venv module is available
if ! python3 -c "import venv" &> /dev/null; then
    echo -e "${RED}Error: venv module is not available.${NC}"
    echo "You may need to install python3-venv package:"
    echo "  Ubuntu/Debian: sudo apt-get install python3-venv"
    echo "  Fedora: sudo dnf install python3-venv"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating .venv...${NC}"
    python3 -m venv .venv
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Virtual environment created successfully!${NC}"
    else
        echo -e "${RED}Failed to create virtual environment.${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}Virtual environment already exists.${NC}"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to activate virtual environment.${NC}"
    exit 1
fi

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo -e "${YELLOW}requirements.txt not found. Creating with necessary dependencies...${NC}"
    cat > requirements.txt << EOF
blessed>=1.19.0
EOF
fi

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Dependencies installed successfully!${NC}"
else
    echo -e "${RED}Failed to install dependencies.${NC}"
    exit 1
fi

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo -e "${RED}Error: main.py not found in current directory.${NC}"
    echo "Make sure you're running this script from the VimWizards project directory."
    exit 1
fi

# Launch the game
echo
echo -e "${GREEN}Setup complete! Launching VimWizards...${NC}"
echo "======================================"
echo

python main.py

# Deactivate virtual environment when game exits
deactivate 2>/dev/null || true
