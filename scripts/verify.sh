#!/bin/bash
# Verification script for Engineering Team Agent

set -e

echo "🔍 Verifying Engineering Team Agent setup..."

# Check Python version
echo "🐍 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.12"
if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.12 or higher is required. Found: $python_version"
    exit 1
fi
echo "✅ Python version: $python_version"

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Run: make setup"
    exit 1
fi
echo "✅ .env file exists"

# Check if API keys are set
if grep -q "your_openai_api_key_here" .env; then
    echo "⚠️  Warning: OPENAI_API_KEY appears to be a placeholder"
fi

if grep -q "your_anthropic_api_key_here" .env; then
    echo "⚠️  Warning: ANTHROPIC_API_KEY appears to be a placeholder"
fi

# Check if Docker is running (for Docker deployment)
if command -v docker &> /dev/null; then
    if docker info &> /dev/null; then
        echo "✅ Docker is running"
    else
        echo "⚠️  Warning: Docker is installed but not running"
    fi
else
    echo "ℹ️  Docker is not installed (optional for local development)"
fi

# Check if uv is installed
if command -v uv &> /dev/null; then
    echo "✅ uv is installed"
else
    echo "⚠️  Warning: uv is not installed. Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"
fi

# Check if output directory exists
if [ ! -d "output" ]; then
    echo "📁 Creating output directory..."
    mkdir -p output
fi
echo "✅ Output directory exists"

echo ""
echo "✅ Verification complete!"
