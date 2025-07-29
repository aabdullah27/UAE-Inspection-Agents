from google.adk.agents import LlmAgent
from main_agent.core.config import settings
from main_agent.prompts.instructions import (
    VIDEO_ANALYSIS_AGENT_INSTRUCTION,
    AUDIO_ANALYSIS_AGENT_INSTRUCTION,
    TEXT_ANALYSIS_AGENT_INSTRUCTION
)

video_analysis_agent = LlmAgent(
    name="VideoAnalysisAgent",
    model=settings.VISION_MODEL,
    instruction=VIDEO_ANALYSIS_AGENT_INSTRUCTION,
    description="Analyzes video evidence from classroom observations if available.",
    output_key="video_analysis_summary"
)

audio_analysis_agent = LlmAgent(
    name="AudioAnalysisAgent",
    model=settings.TEXT_MODEL,
    instruction=AUDIO_ANALYSIS_AGENT_INSTRUCTION,
    description="Analyzes audio evidence from classroom recordings if available.",
    output_key="audio_analysis_summary"
)

text_analysis_agent = LlmAgent(
    name="TextAnalysisAgent",
    model=settings.TEXT_MODEL,
    instruction=TEXT_ANALYSIS_AGENT_INSTRUCTION,
    description="Analyzes textual evidence like notes and documents if available.",
    output_key="text_analysis_summary"
)