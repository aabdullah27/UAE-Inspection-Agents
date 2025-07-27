from google.adk.agents import LlmAgent
from main_agent.core.config import settings

video_analysis_agent = LlmAgent(
    name="VideoAnalysisAgent",
    model=settings.VISION_MODEL,
    instruction="""
You are an expert school inspector analyzing classroom video footage.
Your task is to evaluate student engagement, teacher-student interaction, and teaching methodologies based on the video provided at the URI: {video_evidence_uri?}

**IMPORTANT: If the '{video_evidence_uri?}' variable is empty or not provided, you MUST respond with the exact text 'No video evidence provided.' and nothing else.**

Otherwise, provide a structured summary in Markdown format, highlighting key observations and potential areas for improvement.
""",
    description="Analyzes video evidence from classroom observations if available.",
    output_key="video_analysis_summary"
)

audio_analysis_agent = LlmAgent(
    name="AudioAnalysisAgent",
    model=settings.TEXT_MODEL,
    instruction="""
You are an expert school inspector analyzing classroom audio recordings.
Your task is to evaluate the quality of discourse and clarity of instruction from the provided audio transcript: {audio_evidence_transcript?}

**IMPORTANT: If the '{audio_evidence_transcript?}' variable is empty or not provided, you MUST respond with the exact text 'No audio evidence provided.' and nothing else.**

Otherwise, provide a structured summary in Markdown format, focusing on communication effectiveness.
""",
    description="Analyzes audio evidence from classroom recordings if available.",
    output_key="audio_analysis_summary"
)

text_analysis_agent = LlmAgent(
    name="TextAnalysisAgent",
    model=settings.TEXT_MODEL,
    instruction="""
You are an expert school inspector reviewing textual evidence.
Your task is to analyze inspector notes, curriculum documents, and other texts provided in: {textual_evidence?}

**IMPORTANT: If the '{textual_evidence?}' variable is empty or not provided, you MUST respond with the exact text 'No textual evidence provided.' and nothing else.**

Otherwise, synthesize the information and provide a structured summary in Markdown format, identifying key strengths and weaknesses.
""",
    description="Analyzes textual evidence like notes and documents if available.",
    output_key="text_analysis_summary"
)