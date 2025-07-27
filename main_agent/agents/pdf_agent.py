from google.adk.agents import LlmAgent
from main_agent.core.config import settings
from main_agent.tools.pdf_generator import create_pdf_report

# This agent has one, and only one, job.
pdf_generator_agent = LlmAgent(
    name="PdfGeneratorAgent",
    model=settings.TEXT_MODEL,
    instruction="""
You have been given the final text of a school inspection report.
Your single task is to call the `create_pdf_report` tool with the provided final report text.
Do not add, edit, or change the text.
Do not output anything else.
Your final response MUST be ONLY the result from calling the `create_pdf_report` tool.

Final Report Text:
{final_report_text?}
""",
    description="Takes final report text and generates a PDF using a tool.",
    tools=[create_pdf_report],
    output_key="final_report_pdf_path"
)