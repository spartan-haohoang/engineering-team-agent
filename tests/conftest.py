"""Pytest configuration and fixtures."""

import os
import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
from crewai import Crew, Agent, Task

# Set test environment variables
os.environ["OPENAI_API_KEY"] = "test-key-12345"
os.environ["ANTHROPIC_API_KEY"] = "test-anthropic-key-12345"


@pytest.fixture
def test_output_dir(tmp_path):
    """Create a temporary output directory."""
    output_dir = tmp_path / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


@pytest.fixture
def sample_requirements():
    """Sample requirements for testing."""
    return """
    A simple account management system.
    The system should allow users to create an account and deposit funds.
    """


@pytest.fixture
def mock_crew(monkeypatch):
    """Mock CrewAI crew for testing."""
    mock_crew_instance = MagicMock(spec=Crew)
    mock_result = MagicMock()
    mock_result.raw = "Test result"
    mock_crew_instance.kickoff.return_value = mock_result

    def mock_crew_init(*args, **kwargs):
        return mock_crew_instance

    monkeypatch.setattr("engineering_team_agent.crew.Crew", mock_crew_init)
    return mock_crew_instance


@pytest.fixture
def mock_engineering_team(monkeypatch):
    """Mock EngineeringTeam class."""
    mock_team = MagicMock()
    mock_team.crew.return_value = MagicMock()
    mock_team.crew.return_value.kickoff.return_value = MagicMock()
    return mock_team
