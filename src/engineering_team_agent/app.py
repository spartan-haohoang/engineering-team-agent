"""Streamlit UI for the Engineering Team Agent."""

import os
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

from engineering_team_agent.main import run

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Engineering Team Agent",
    page_icon="👷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .agent-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def check_api_keys():
    """Check if required API keys are set."""
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    if not openai_key or openai_key == "your_openai_api_key_here":
        return False, "OpenAI API key is not set"
    if not anthropic_key or anthropic_key == "your_anthropic_api_key_here":
        return False, "Anthropic API key is not set (required for backend/frontend/test engineers)"
    return True, "All API keys are set"


def main():
    """Main Streamlit application."""
    # Header
    st.markdown('<div class="main-header">👷 Engineering Team Agent</div>', unsafe_allow_html=True)
    st.markdown(
        "A 4-agent system that designs, builds, tests, and creates UI for software modules using CrewAI."
    )

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")

        # API Key Check
        api_ok, api_message = check_api_keys()
        if api_ok:
            st.success("✅ " + api_message)
        else:
            st.error("❌ " + api_message)
            st.info("Please set your API keys in the `.env` file")

        st.divider()

        # Default values
        default_module = os.getenv("DEFAULT_MODULE_NAME", "accounts.py")
        default_class = os.getenv("DEFAULT_CLASS_NAME", "Account")

        module_name = st.text_input("Module Name", value=default_module, help="e.g., accounts.py")
        class_name = st.text_input("Class Name", value=default_class, help="e.g., Account")

        st.divider()
        st.markdown("### 📚 About")
        st.markdown(
            """
            This application uses 4 AI agents:
            1. **Engineering Lead** - Creates detailed designs
            2. **Backend Engineer** - Implements the code
            3. **Frontend Engineer** - Creates Gradio UI
            4. **Test Engineer** - Writes unit tests
            """
        )

    # Main content
    st.header("📝 Requirements")

    # Default requirements
    default_requirements = """A simple account management system for a trading simulation platform.
The system should allow users to create an account, deposit funds, and withdraw funds.
The system should allow users to record that they have bought or sold shares, providing a quantity.
The system should calculate the total value of the user's portfolio, and the profit or loss from the initial deposit.
The system should be able to report the holdings of the user at any point in time.
The system should be able to report the profit or loss of the user at any point in time.
The system should be able to list the transactions that the user has made over time.
The system should prevent the user from withdrawing funds that would leave them with a negative balance, or
from buying more shares than they can afford, or selling shares that they don't have.
The system has access to a function get_share_price(symbol) which returns the current price of a share, 
and includes a test implementation that returns fixed prices for AAPL, TSLA, GOOGL."""

    requirements = st.text_area(
        "Enter your requirements:",
        value=default_requirements,
        height=200,
        help="Describe what you want the software module to do",
    )

    # Run button
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        run_button = st.button("🚀 Run Engineering Team", type="primary", use_container_width=True)
    with col2:
        clear_button = st.button("🗑️ Clear Output", use_container_width=True)

    if clear_button:
        st.session_state.output = None
        st.session_state.error = None
        st.rerun()

    # Display output
    if run_button:
        if not api_ok:
            st.error("❌ Please set your API keys in the `.env` file before running")
            return

        if not requirements.strip():
            st.error("❌ Please enter requirements")
            return

        # Show progress
        with st.spinner("🤖 Engineering team is working... This may take a few minutes."):
            try:
                result = run(
                    requirements=requirements,
                    module_name=module_name,
                    class_name=class_name,
                )

                if result["success"]:
                    st.session_state.output = result
                    st.session_state.error = None
                else:
                    st.session_state.error = result.get("error", "Unknown error")
                    st.session_state.output = None
            except Exception as e:
                st.session_state.error = str(e)
                st.session_state.output = None

    # Display results
    if "output" in st.session_state and st.session_state.output:
        st.success("✅ Engineering team completed successfully!")
        st.markdown(f"**Output directory:** `{st.session_state.output['output_dir']}`")

        output_dir = Path(st.session_state.output["output_dir"])

        # Show generated files
        st.header("📄 Generated Files")

        # Design document
        design_file = output_dir / f"{module_name.replace('.py', '')}_design.md"
        if design_file.exists():
            with st.expander("📋 Design Document", expanded=False):
                st.code(design_file.read_text(), language="markdown")

        # Code file
        code_file = output_dir / module_name
        if code_file.exists():
            with st.expander(f"💻 {module_name}", expanded=True):
                st.code(code_file.read_text(), language="python")

        # Test file
        test_file = output_dir / f"test_{module_name}"
        if test_file.exists():
            with st.expander(f"🧪 test_{module_name}", expanded=False):
                st.code(test_file.read_text(), language="python")

        # UI file
        ui_file = output_dir / "app.py"
        if ui_file.exists():
            with st.expander("🎨 Gradio UI (app.py)", expanded=False):
                st.code(ui_file.read_text(), language="python")

    if "error" in st.session_state and st.session_state.error:
        st.error(f"❌ Error: {st.session_state.error}")


if __name__ == "__main__":
    main()
