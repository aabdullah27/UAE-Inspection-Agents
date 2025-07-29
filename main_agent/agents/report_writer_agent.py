from google.adk.agents import LlmAgent
from main_agent.core.config import settings
from main_agent.tools.date_tool import get_current_date
from main_agent.tools.pdf_generator import create_pdf_report
from main_agent.prompts.instructions import REPORT_WRITER_AGENT_INSTRUCTION

report_writer_agent = LlmAgent(
    name="FinalReportAgent",
    model=settings.TEXT_MODEL,
    instruction=REPORT_WRITER_AGENT_INSTRUCTION,
    description="Generates the final inspection report and saves it as a PDF.",
    output_key="final_report",
    tools=[get_current_date, create_pdf_report]
)