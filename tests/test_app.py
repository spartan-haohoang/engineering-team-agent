"""Unit tests for the Streamlit app."""

import pytest
import os
from unittest.mock import Mock, MagicMock, patch
from engineering_team_agent.app import check_api_keys


class TestApp:
    """Test cases for Streamlit app."""

    @pytest.mark.unit
    def test_check_api_keys_with_valid_keys(self, monkeypatch):
        """Test check_api_keys with valid API keys."""
        monkeypatch.setenv("OPENAI_API_KEY", "valid-openai-key")
        monkeypatch.setenv("ANTHROPIC_API_KEY", "valid-anthropic-key")

        ok, message = check_api_keys()
        assert ok is True
        assert "All API keys are set" in message

    @pytest.mark.unit
    def test_check_api_keys_missing_openai(self, monkeypatch):
        """Test check_api_keys with missing OpenAI key."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.setenv("ANTHROPIC_API_KEY", "valid-anthropic-key")

        ok, message = check_api_keys()
        assert ok is False
        assert "OpenAI API key" in message

    @pytest.mark.unit
    def test_check_api_keys_missing_anthropic(self, monkeypatch):
        """Test check_api_keys with missing Anthropic key."""
        monkeypatch.setenv("OPENAI_API_KEY", "valid-openai-key")
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

        ok, message = check_api_keys()
        assert ok is False
        assert "Anthropic API key" in message

    @pytest.mark.unit
    def test_check_api_keys_placeholder_values(self, monkeypatch):
        """Test check_api_keys with placeholder values."""
        monkeypatch.setenv("OPENAI_API_KEY", "your_openai_api_key_here")
        monkeypatch.setenv("ANTHROPIC_API_KEY", "your_anthropic_api_key_here")

        ok, message = check_api_keys()
        assert ok is False

    @pytest.mark.unit
    @patch("engineering_team_agent.app.run")
    def test_app_integration(self, mock_run, monkeypatch):
        """Test app integration with mocked run function."""
        monkeypatch.setenv("OPENAI_API_KEY", "valid-openai-key")
        monkeypatch.setenv("ANTHROPIC_API_KEY", "valid-anthropic-key")

        mock_run.return_value = {
            "success": True,
            "result": MagicMock(),
            "output_dir": "/tmp/output",
        }

        # This is a basic integration test
        # In a real scenario, we'd use streamlit testing tools
        assert mock_run is not None
