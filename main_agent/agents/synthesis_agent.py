# main_agent/agents/synthesis_agent.py
from google.adk.agents import LlmAgent
from main_agent.core.config import settings

synthesis_agent = LlmAgent(
    name="SynthesisAgent",
    model=settings.TEXT_MODEL,
    instruction="""
You are a lead school inspector responsible for consolidating findings from different evidence sources.
You have received up to three analysis reports. Some reports may contain the phrase 'No evidence provided.' You must completely ignore any summary that consists solely of such a phrase.

Synthesize a single, cohesive "Preliminary Findings" document based ONLY on the valid, detailed reports you have received. If no valid reports are provided, state that there was insufficient evidence to form a preliminary finding.

Here are the reports:
Video Analysis:
{video_analysis_summary}

Audio Analysis:
{audio_analysis_summary}

Textual Analysis:
{text_analysis_summary}
""",
    description="Synthesizes findings from available analysis reports into a preliminary summary.",
    output_key="preliminary_findings"
)