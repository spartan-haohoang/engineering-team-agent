# 👷 Engineering Team Agent

A production-ready 4-agent system that designs, builds, tests, and creates UI for software modules using CrewAI. This application deploys an autonomous engineering team that can take high-level requirements and produce complete, tested software solutions.

## ✨ Features

- **4-Agent System**: Engineering Lead, Backend Engineer, Frontend Engineer, and Test Engineer
- **Complete Workflow**: From requirements to design, code, tests, and UI
- **Docker Support**: Fully containerized with Docker and Docker Compose
- **Streamlit UI**: Beautiful, modern web interface for easy interaction
- **Code Execution**: Safe code execution using Docker containers
- **Production Ready**: Includes health checks, error handling, and best practices
- **TDD Tests**: Comprehensive test suite with unit and integration tests

## 🏗️ Architecture

The Engineering Team consists of 4 specialized agents:

1. **Engineering Lead** (GPT-4o) - Creates detailed design documents
2. **Backend Engineer** (Claude 3.7 Sonnet) - Implements the Python module
3. **Frontend Engineer** (Claude 3.7 Sonnet) - Creates Gradio UI
4. **Test Engineer** (Claude 3.7 Sonnet) - Writes comprehensive unit tests

## 📋 Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended) or pip
- Docker and Docker Compose (for containerized deployment and code execution)
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))
- Anthropic API key ([get one here](https://console.anthropic.com/)) - Required for backend, frontend, and test engineers

## 🚀 Quick Start

### Option 1: Using Docker (Recommended)

1. **Clone or navigate to the project directory:**
   ```bash
   cd engineering-team-agent
   ```

2. **Create environment file:**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys:
   # - OPENAI_API_KEY
   # - ANTHROPIC_API_KEY
   ```

3. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

4. **Access the application:**
   - Open your browser to `http://localhost:8501`

### Option 2: Local Development

1. **Install uv (if not already installed):**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Navigate to project directory:**
   ```bash
   cd engineering-team-agent
   ```

3. **Create and activate virtual environment:**
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   uv sync
   ```

5. **Create environment file:**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

6. **Run the application:**
   ```bash
   uv run streamlit run src/engineering_team_agent/app.py
   ```

7. **Access the application:**
   - Open your browser to `http://localhost:8501`

## 📁 Project Structure

```
engineering-team-agent/
├── src/
│   └── engineering_team_agent/
│       ├── __init__.py
│       ├── app.py              # Streamlit UI application
│       ├── main.py              # Main entry point
│       ├── crew.py              # CrewAI crew definition
│       ├── config/
│       │   ├── agents.yaml      # Agent configurations
│       │   └── tasks.yaml       # Task configurations
│       └── tools/
│           ├── __init__.py
│           └── custom_tool.py   # Custom tools example
├── tests/                       # Test suite
│   ├── conftest.py
│   ├── test_crew.py
│   ├── test_main.py
│   ├── test_app.py
│   └── test_integration.py
├── output/                      # Generated files (created at runtime)
├── knowledge/                   # Knowledge base files
│   └── user_preference.txt
├── scripts/                     # Utility scripts
├── Dockerfile                   # Docker image definition
├── docker-compose.yml           # Docker Compose configuration
├── pyproject.toml               # Python project configuration (uv)
├── pytest.ini                   # Pytest configuration
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── Makefile                     # Make commands
└── README.md                    # This file
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional
STREAMLIT_PORT=8501
DEFAULT_MODULE_NAME=accounts.py
DEFAULT_CLASS_NAME=Account
CREWAI_VERBOSE=true
CREWAI_MAX_EXECUTION_TIME=500
CREWAI_MAX_RETRY_LIMIT=3
```

### Knowledge Base

You can customize agent behavior by editing `knowledge/user_preference.txt` with user preferences and context.

## 🐳 Docker Commands

### Build the image:
```bash
docker-compose build
```

### Run the container:
```bash
docker-compose up
```

### Run in detached mode:
```bash
docker-compose up -d
```

### View logs:
```bash
docker-compose logs -f
```

### Stop the container:
```bash
docker-compose down
```

### Rebuild after code changes:
```bash
docker-compose up --build
```

## 🛠️ Development

### Using uv (Recommended)

```bash
# Install dependencies
uv sync

# Install with dev dependencies
uv sync --dev

# Run the app
uv run streamlit run src/engineering_team_agent/app.py

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov

# Format code
uv run black src/ tests/

# Lint code
uv run ruff check src/ tests/
```

### Using pip (Alternative)

```bash
# Install dependencies
pip install -e .

# Install with dev dependencies
pip install -e ".[dev]"

# Run the app
streamlit run src/engineering_team_agent/app.py

# Run tests
pytest
```

### Using Make

```bash
# Show all available commands
make help

# Setup environment
make setup

# Install dependencies
make install

# Run locally
make run

# Docker commands
make docker-build
make docker-up
make docker-down
make docker-logs
```

## 📝 How It Works

1. **Requirements Input**: User provides high-level requirements for a software module
2. **Design Phase**: Engineering Lead creates a detailed design document
3. **Implementation Phase**: Backend Engineer writes the Python module
4. **UI Phase**: Frontend Engineer creates a Gradio UI
5. **Testing Phase**: Test Engineer writes comprehensive unit tests
6. **Output**: All files are saved to the `output/` directory

### Example Workflow

1. Enter requirements in the Streamlit UI
2. Specify module name (e.g., `accounts.py`) and class name (e.g., `Account`)
3. Click "Run Engineering Team"
4. Wait for the agents to complete their work (may take 5-10 minutes)
5. Review generated files:
   - `{module_name}_design.md` - Design document
   - `{module_name}` - Python module
   - `test_{module_name}` - Unit tests
   - `app.py` - Gradio UI

## 🧪 Testing

The project includes comprehensive tests:

```bash
# Run all tests
pytest

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run with coverage
pytest --cov

# Run specific test file
pytest tests/test_crew.py
```

## 🔒 Security Best Practices

- Never commit your `.env` file to version control
- Keep your API keys secure and rotate them regularly
- Use environment variables for all sensitive data
- Review the `.gitignore` file to ensure sensitive files are excluded
- The Docker setup uses safe code execution mode with Docker containers

## 🐛 Troubleshooting

### Issue: "OPENAI_API_KEY not set"
**Solution**: Make sure you've created a `.env` file with your API key:
```bash
cp .env.example .env
# Edit .env and add your keys
```

### Issue: "ANTHROPIC_API_KEY not set"
**Solution**: The Anthropic API key is required for backend, frontend, and test engineers. Add it to your `.env` file.

### Issue: Docker build fails
**Solution**: 
- Make sure Docker is running
- Check that you have enough disk space
- Try rebuilding: `docker-compose build --no-cache`

### Issue: Port already in use
**Solution**: Change the port in `docker-compose.yml` or `.env`:
```yaml
ports:
  - "8502:8501"  # Use port 8502 instead
```

### Issue: Code execution fails / "Docker is not installed" error / "mounts denied" error
**Solution**: 

**For macOS with Docker Desktop:**
- Code execution is **disabled by default** due to Docker Desktop path mounting restrictions
- The agents will still write code, but won't execute it (this is usually fine for the engineering team use case)
- To enable code execution on macOS:
  1. Open Docker Desktop
  2. Go to Settings → Resources → File Sharing
  3. Add `/tmp` or `/var/folders` to shared paths
  4. Restart Docker Desktop
  5. Set `ENABLE_CODE_EXECUTION=true` in your `.env` file
  6. Restart the container: `docker-compose restart`

**For Linux:**
- Ensure Docker is running: `docker ps` should work
- Verify Docker socket is accessible
- You may need: `sudo usermod -aG docker $USER` then log out/in
- Set `ENABLE_CODE_EXECUTION=true` in your `.env` file

**Note:** Code execution is optional - the engineering team agents can write code without executing it. The code will still be generated and saved to the `output/` directory.

### Issue: Agents taking too long
**Solution**: 
- This is normal - the full workflow can take 5-10 minutes
- Check API rate limits
- Consider using faster models for development

## 📚 API Costs

This application uses multiple AI APIs, which incur costs based on usage:

- **OpenAI GPT-4o**: ~$2.50 per 1M input tokens, ~$10 per 1M output tokens
- **Anthropic Claude 3.7 Sonnet**: Check [Anthropic pricing](https://www.anthropic.com/pricing)

Monitor your usage at:
- [OpenAI's usage dashboard](https://platform.openai.com/usage)
- [Anthropic's usage dashboard](https://console.anthropic.com/)

## 🤝 Contributing

This is a project from "The Complete Agent & MCP Course", but suggestions and improvements are welcome!

## 📄 License

This project is part of "The Complete Agent & MCP Course" educational content.

## 🙏 Acknowledgments

- Built as part of Project 5 from "The Complete Agent & MCP Course"
- Uses [CrewAI](https://crewai.com) for multi-agent orchestration
- Uses OpenAI and Anthropic APIs for AI capabilities
- Streamlit for the web interface
- uv for fast Python package management

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the course materials
3. Check [CrewAI documentation](https://docs.crewai.com)
4. Check OpenAI and Anthropic API documentation

---

**Happy building! 🚀**
