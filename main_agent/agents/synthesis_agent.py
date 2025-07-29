from google.adk.agents import LlmAgent
from main_agent.core.config import settings
from main_agent.tools.rag_orchestrator import retrieve_from_collection
from main_agent.prompts.instructions import SYNTHESIS_AGENT_INSTRUCTION

synthesis_agent = LlmAgent(
    name="SynthesisAgent",
    model=settings.TEXT_MODEL,
    instruction=SYNTHESIS_AGENT_INSTRUCTION,
    description="Consolidates analysis summaries, retrieves framework context, and outputs an evaluated findings report.",
    tools=[retrieve_from_collection],
    output_key="evaluated_findings"
)