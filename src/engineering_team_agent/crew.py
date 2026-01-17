"""Engineering Team Crew - 4-agent system for software development."""

import os
import warnings
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Suppress warnings from dependencies
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Check if code execution should be enabled
# Set ENABLE_CODE_EXECUTION=false to disable (useful for Docker Desktop on macOS)
ENABLE_CODE_EXECUTION = os.getenv("ENABLE_CODE_EXECUTION", "true").lower() == "true"


@CrewBase
class EngineeringTeam:
    """EngineeringTeam crew with 4 agents: Lead, Backend, Frontend, and Test Engineer."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def engineering_lead(self) -> Agent:
        """Engineering Lead agent that creates detailed designs."""
        return Agent(
            config=self.agents_config["engineering_lead"],
            verbose=True,
        )

    @agent
    def backend_engineer(self) -> Agent:
        """Backend Engineer agent that implements the design."""
        agent_config = {
            "config": self.agents_config["backend_engineer"],
            "verbose": True,
        }
        # Only enable code execution if explicitly enabled
        # Note: Code execution may not work on Docker Desktop (macOS) due to path mounting restrictions
        if ENABLE_CODE_EXECUTION:
            agent_config.update({
                "allow_code_execution": True,
                "code_execution_mode": "safe",  # Uses Docker for safety
                "max_execution_time": 500,
                "max_retry_limit": 3,
            })
        return Agent(**agent_config)

    @agent
    def frontend_engineer(self) -> Agent:
        """Frontend Engineer agent that creates Gradio UI."""
        return Agent(
            config=self.agents_config["frontend_engineer"],
            verbose=True,
        )

    @agent
    def test_engineer(self) -> Agent:
        """Test Engineer agent that writes unit tests."""
        agent_config = {
            "config": self.agents_config["test_engineer"],
            "verbose": True,
        }
        # Only enable code execution if explicitly enabled
        if ENABLE_CODE_EXECUTION:
            agent_config.update({
                "allow_code_execution": True,
                "code_execution_mode": "safe",  # Uses Docker for safety
                "max_execution_time": 500,
                "max_retry_limit": 3,
            })
        return Agent(**agent_config)

    @task
    def design_task(self) -> Task:
        """Task for creating the design document."""
        return Task(config=self.tasks_config["design_task"])

    @task
    def code_task(self) -> Task:
        """Task for implementing the backend code."""
        return Task(config=self.tasks_config["code_task"])

    @task
    def frontend_task(self) -> Task:
        """Task for creating the frontend UI."""
        return Task(config=self.tasks_config["frontend_task"])

    @task
    def test_task(self) -> Task:
        """Task for writing unit tests."""
        return Task(config=self.tasks_config["test_task"])

    @crew
    def crew(self) -> Crew:
        """Creates the engineering team crew."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
