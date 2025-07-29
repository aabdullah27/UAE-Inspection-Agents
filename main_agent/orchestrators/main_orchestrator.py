from google.adk.agents import SequentialAgent, ParallelAgent

from main_agent.agents.analysis_agents import (
    video_analysis_agent,
    audio_analysis_agent,
    text_analysis_agent
)
from main_agent.agents.synthesis_agent import synthesis_agent
from main_agent.agents.report_writer_agent import report_writer_agent

# Parallel analysis orchestrator remains the same
analysis_orchestrator = ParallelAgent(
    name="EvidenceAnalysisOrchestrator",
    sub_agents=[
        video_analysis_agent,
        audio_analysis_agent,
        text_analysis_agent
    ],
    description="Runs specialized agents to analyze video, audio, and text evidence in parallel."
)

# The main SequentialAgent with the final steps
inspection_pipeline_agent = SequentialAgent(
    name="SchoolInspectionPipeline",
    sub_agents=[
        analysis_orchestrator,
        synthesis_agent,
        report_writer_agent
    ],
    description="Orchestrates the end-to-end school inspection and report generation process."
)