#!/bin/bash
# Setup script for Engineering Team Agent

set -e

echo "🚀 Setting up Engineering Team Agent..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file. Please edit it with your API keys."
else
    echo "ℹ️  .env file already exists."
fi

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo "✅ uv installed. Please restart your terminal or run: source ~/.bashrc"
else
    echo "✅ uv is already installed."
fi

# Create output directory
echo "📁 Creating output directory..."
mkdir -p output
echo "✅ Output directory created."

# Create knowledge directory if it doesn't exist
if [ ! -d "knowledge" ]; then
    echo "📁 Creating knowledge directory..."
    mkdir -p knowledge
    echo "✅ Knowledge directory created."
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your API keys:"
echo "   - OPENAI_API_KEY"
echo "   - ANTHROPIC_API_KEY"
echo "2. Install dependencies: make install"
echo "3. Run the application: make run"
echo "   Or use Docker: make docker-build && make docker-up"
