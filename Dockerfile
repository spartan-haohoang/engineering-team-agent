# Use Python 3.12 slim image
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Docker CLI using static binary from GitHub releases
# Using a specific version for reliability
RUN ARCH=$(uname -m) \
    && if [ "$ARCH" = "x86_64" ]; then DOCKER_ARCH="x86_64"; \
    elif [ "$ARCH" = "aarch64" ]; then DOCKER_ARCH="aarch64"; \
    else DOCKER_ARCH="x86_64"; fi \
    && DOCKER_VERSION="25.0.3" \
    && curl -fsSL "https://download.docker.com/linux/static/stable/${DOCKER_ARCH}/docker-${DOCKER_VERSION}.tgz" -o /tmp/docker.tgz \
    && tar -xz -C /tmp -f /tmp/docker.tgz \
    && mv /tmp/docker/docker /usr/local/bin/docker \
    && chmod +x /usr/local/bin/docker \
    && rm -rf /tmp/docker* \
    && docker --version || echo "Warning: Docker CLI may not be available"

# Set working directory
WORKDIR /app

# Install uv for fast Python package management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set environment variables
ENV UV_SYSTEM_PYTHON=1 \
    UV_NO_CACHE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src

# Copy project files needed for installation
COPY pyproject.toml ./
COPY README.md ./

# Install dependencies using uv
RUN uv pip install --system --no-cache-dir -e .

# Copy application code
COPY src/ ./src/
COPY knowledge/ ./knowledge/
COPY scripts/ ./scripts/

# Create output directory
RUN mkdir -p /app/output

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Streamlit app
CMD ["python", "-m", "streamlit", "run", "src/engineering_team_agent/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
