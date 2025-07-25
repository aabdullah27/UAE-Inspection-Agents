from google.adk.agents import Agent
# from google.adk.tools import google_search
from main_agent.tools.rag_orchestrator import retrieve_from_collection
from main_agent.prompts.instructions import MAIN_AGENT_INSTRUCTIONS

root_agent = Agent(
    name="main_agent",
    description="A main agent that is the inspector working for both the school and the inspection team",
    model="gemini-2.5-flash",
    tools=[retrieve_from_collection],
    instruction=MAIN_AGENT_INSTRUCTIONS
)