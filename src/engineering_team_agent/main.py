"""Main entry point for the Engineering Team Agent."""

import os
import sys
import warnings
from pathlib import Path
from typing import Optional

from engineering_team_agent.crew import EngineeringTeam

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run(
    requirements: str,
    module_name: str = "accounts.py",
    class_name: str = "Account",
    output_dir: Optional[str] = None,
) -> dict:
    """
    Run the engineering team crew to build, test, and create UI for a software module.

    Args:
        requirements: High-level requirements for the software module
        module_name: Name of the Python module to create (e.g., "accounts.py")
        class_name: Name of the main class in the module
        output_dir: Directory to save output files (defaults to ./output)

    Returns:
        Dictionary with execution results
    """
    # Create output directory if it doesn't exist
    if output_dir is None:
        output_dir = Path(__file__).parent.parent.parent.parent / "output"
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    # Prepare inputs for the crew
    inputs = {
        "requirements": requirements,
        "module_name": module_name,
        "class_name": class_name,
    }

    try:
        # Create and run the crew
        crew_instance = EngineeringTeam()
        result = crew_instance.crew().kickoff(inputs=inputs)

        return {
            "success": True,
            "result": result,
            "output_dir": str(output_dir),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "output_dir": str(output_dir),
        }


if __name__ == "__main__":
    # Example usage
    requirements = """
    A simple account management system for a trading simulation platform.
    The system should allow users to create an account, deposit funds, and withdraw funds.
    The system should allow users to record that they have bought or sold shares, providing a quantity.
    The system should calculate the total value of the user's portfolio, and the profit or loss from the initial deposit.
    The system should be able to report the holdings of the user at any point in time.
    The system should be able to report the profit or loss of the user at any point in time.
    The system should be able to list the transactions that the user has made over time.
    The system should prevent the user from withdrawing funds that would leave them with a negative balance, or
    from buying more shares than they can afford, or selling shares that they don't have.
    The system has access to a function get_share_price(symbol) which returns the current price of a share, 
    and includes a test implementation that returns fixed prices for AAPL, TSLA, GOOGL.
    """
    module_name = "accounts.py"
    class_name = "Account"

    result = run(requirements, module_name, class_name)
    if result["success"]:
        print(f"✅ Success! Output saved to {result['output_dir']}")
    else:
        print(f"❌ Error: {result['error']}")
        sys.exit(1)
