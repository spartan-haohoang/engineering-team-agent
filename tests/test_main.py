"""Unit tests for the main module."""

import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
from engineering_team_agent.main import run


class TestMain:
    """Test cases for main module."""

    @pytest.mark.unit
    def test_run_with_valid_inputs(self, test_output_dir, sample_requirements, mock_crew):
        """Test run function with valid inputs."""
        with patch("engineering_team_agent.main.EngineeringTeam") as mock_team_class:
            mock_team = MagicMock()
            mock_crew_instance = MagicMock()
            mock_result = MagicMock()
            mock_result.raw = "Test result"
            mock_crew_instance.kickoff.return_value = mock_result
            mock_team.crew.return_value = mock_crew_instance
            mock_team_class.return_value = mock_team

            result = run(
                requirements=sample_requirements,
                module_name="test.py",
                class_name="Test",
                output_dir=str(test_output_dir),
            )

            assert result["success"] is True
            assert "result" in result
            assert "output_dir" in result
            assert str(test_output_dir) in result["output_dir"]

    @pytest.mark.unit
    def test_run_creates_output_directory(self, tmp_path, sample_requirements, mock_crew):
        """Test that run creates output directory if it doesn't exist."""
        output_dir = tmp_path / "new_output"
        assert not output_dir.exists()

        with patch("engineering_team_agent.main.EngineeringTeam") as mock_team_class:
            mock_team = MagicMock()
            mock_crew_instance = MagicMock()
            mock_result = MagicMock()
            mock_crew_instance.kickoff.return_value = mock_result
            mock_team.crew.return_value = mock_crew_instance
            mock_team_class.return_value = mock_team

            result = run(
                requirements=sample_requirements,
                module_name="test.py",
                class_name="Test",
                output_dir=str(output_dir),
            )

            assert output_dir.exists()
            assert result["success"] is True

    @pytest.mark.unit
    def test_run_with_default_output_dir(self, sample_requirements, mock_crew):
        """Test run with default output directory."""
        with patch("engineering_team_agent.main.EngineeringTeam") as mock_team_class:
            mock_team = MagicMock()
            mock_crew_instance = MagicMock()
            mock_result = MagicMock()
            mock_crew_instance.kickoff.return_value = mock_result
            mock_team.crew.return_value = mock_crew_instance
            mock_team_class.return_value = mock_team

            result = run(
                requirements=sample_requirements,
                module_name="test.py",
                class_name="Test",
            )

            assert result["success"] is True
            assert "output_dir" in result

    @pytest.mark.unit
    def test_run_handles_exceptions(self, test_output_dir, sample_requirements):
        """Test run handles exceptions gracefully."""
        with patch("engineering_team_agent.main.EngineeringTeam") as mock_team_class:
            mock_team = MagicMock()
            mock_crew_instance = MagicMock()
            mock_crew_instance.kickoff.side_effect = Exception("Test error")
            mock_team.crew.return_value = mock_crew_instance
            mock_team_class.return_value = mock_team

            result = run(
                requirements=sample_requirements,
                module_name="test.py",
                class_name="Test",
                output_dir=str(test_output_dir),
            )

            assert result["success"] is False
            assert "error" in result
            assert "Test error" in result["error"]

    @pytest.mark.unit
    def test_run_passes_correct_inputs(self, test_output_dir, sample_requirements, mock_crew):
        """Test that run passes correct inputs to crew."""
        with patch("engineering_team_agent.main.EngineeringTeam") as mock_team_class:
            mock_team = MagicMock()
            mock_crew_instance = MagicMock()
            mock_result = MagicMock()
            mock_crew_instance.kickoff.return_value = mock_result
            mock_team.crew.return_value = mock_crew_instance
            mock_team_class.return_value = mock_team

            run(
                requirements=sample_requirements,
                module_name="custom_module.py",
                class_name="CustomClass",
                output_dir=str(test_output_dir),
            )

            # Verify kickoff was called with correct inputs
            call_args = mock_crew_instance.kickoff.call_args
            assert call_args is not None
            inputs = call_args[1]["inputs"]
            assert inputs["requirements"] == sample_requirements
            assert inputs["module_name"] == "custom_module.py"
            assert inputs["class_name"] == "CustomClass"
