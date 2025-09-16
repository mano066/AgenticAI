from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class Idealens():
    """Idealens crew — Insightful, story-driven, and cross-disciplinary thinkers"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def explorer(self) -> Agent:
        return Agent(
            config=self.agents_config['explorer'],  # type: ignore[index]
            verbose=True
        )

    @agent
    def storyteller(self) -> Agent:
        return Agent(
            config=self.agents_config['storyteller'],  # type: ignore[index]
            verbose=True
        )

    @agent
    def synthesizer(self) -> Agent:
        return Agent(
            config=self.agents_config['synthesizer'],  # type: ignore[index]
            verbose=True
        )

    @task
    def explore_task(self) -> Task:
        return Task(
            config=self.tasks_config['explore'],  # type: ignore[index]
            output_file='output/explore.md'
        )

    @task
    def narrate_task(self) -> Task:
        return Task(
            config=self.tasks_config['narrate'],  # type: ignore[index]
            output_file='output/narrate.md'
        )

    @task
    def synthesize_task(self) -> Task:
        return Task(
            config=self.tasks_config['synthesize'],  # type: ignore[index]
            output_file='output/synthesize.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Idealens crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
