#!/bin/bash
# Check Docker availability for CrewAI code execution

echo "🔍 Checking Docker setup for CrewAI code execution..."
echo ""

# Check if running in container
if [ -f /.dockerenv ]; then
    echo "✅ Running inside Docker container"
    
    # Check Docker CLI
    if command -v docker &> /dev/null; then
        echo "✅ Docker CLI is installed"
        docker --version
    else
        echo "❌ Docker CLI is not installed"
        exit 1
    fi
    
    # Check Docker socket
    if [ -S /var/run/docker.sock ]; then
        echo "✅ Docker socket is accessible"
    else
        echo "❌ Docker socket not found at /var/run/docker.sock"
        echo "   Make sure docker-compose.yml mounts the socket"
        exit 1
    fi
    
    # Test Docker connection
    if docker ps &> /dev/null; then
        echo "✅ Docker daemon is accessible"
        echo ""
        echo "📋 Running containers:"
        docker ps --format "table {{.Names}}\t{{.Status}}"
    else
        echo "❌ Cannot connect to Docker daemon"
        echo "   Error: $(docker ps 2>&1)"
        exit 1
    fi
else
    echo "ℹ️  Running on host machine"
    
    # Check Docker
    if command -v docker &> /dev/null; then
        echo "✅ Docker is installed"
        docker --version
        
        if docker ps &> /dev/null; then
            echo "✅ Docker daemon is running"
        else
            echo "❌ Docker daemon is not running"
            echo "   Please start Docker Desktop or Docker Engine"
            exit 1
        fi
    else
        echo "❌ Docker is not installed"
        echo "   Please install Docker Desktop: https://docs.docker.com/desktop/"
        exit 1
    fi
fi

echo ""
echo "✅ Docker setup is correct for CrewAI code execution!"
