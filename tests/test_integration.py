"""Integration tests for the Engineering Team Agent."""

import pytest
from pathlib import Path
from engineering_team_agent.main import run


@pytest.mark.integration
@pytest.mark.slow
class TestIntegration:
    """Integration tests that may require API calls."""

    @pytest.mark.skip(reason="Requires API keys and may take time")
    def test_full_workflow(self, test_output_dir, sample_requirements):
        """Test full workflow from requirements to output."""
        result = run(
            requirements=sample_requirements,
            module_name="test_accounts.py",
            class_name="TestAccount",
            output_dir=str(test_output_dir),
        )

        # This test would require actual API keys
        # For now, we just verify the structure
        assert "success" in result
        assert "output_dir" in result

    @pytest.mark.integration
    def test_output_directory_structure(self, test_output_dir):
        """Test that output directory structure is correct."""
        assert test_output_dir.exists()
        assert test_output_dir.is_dir()
