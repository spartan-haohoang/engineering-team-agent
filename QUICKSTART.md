# 🚀 Quick Start Guide

Get the Engineering Team Agent up and running in minutes!

## Prerequisites

- Docker and Docker Compose installed
- OpenAI API key
- Anthropic API key

## Step 1: Setup Environment

```bash
cd engineering-team-agent
cp .env.example .env
```

Edit `.env` and add your API keys:
```bash
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

## Step 2: Build and Run

```bash
docker-compose up --build
```

## Step 3: Access the Application

Open your browser to: **http://localhost:8501**

## Step 4: Use the Engineering Team

1. Enter your requirements in the text area
2. Specify module name (e.g., `accounts.py`) and class name (e.g., `Account`)
3. Click "🚀 Run Engineering Team"
4. Wait for the agents to complete (5-10 minutes)
5. Review generated files in the `output/` directory

## Alternative: Local Development

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Setup
make setup
make install-dev

# Run
make run
```

## Running Tests

```bash
# Install dev dependencies
make install-dev

# Run tests
make test

# Run with coverage
make test-cov
```

## Troubleshooting

### Container won't start
- Check that Docker is running: `docker ps`
- Check logs: `docker-compose logs`

### API key errors
- Verify your `.env` file has valid API keys
- Make sure `.env` is in the project root

### Port already in use
- Change `STREAMLIT_PORT` in `.env` or `docker-compose.yml`

### "Docker is not installed" or "mounts denied" error
- **Code execution is disabled by default** on macOS (Docker Desktop limitation)
- **This is OK!** The agents will still write code, just won't execute it
- To enable code execution on macOS:
  1. Docker Desktop → Settings → Resources → File Sharing
  2. Add `/tmp` to shared paths
  3. Restart Docker Desktop
  4. Set `ENABLE_CODE_EXECUTION=true` in `.env`
  5. Restart: `docker-compose restart`
- On Linux: Set `ENABLE_CODE_EXECUTION=true` in `.env`

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out the example requirements in the Streamlit UI
- Customize agent behavior in `knowledge/user_preference.txt`

---

**Happy building! 👷**
