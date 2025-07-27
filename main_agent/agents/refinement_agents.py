from google.adk.agents import LlmAgent
from main_agent.core.config import settings

report_critique_agent = LlmAgent(
    name="ReportCritiqueAgent",
    model=settings.TEXT_MODEL,
    instruction="""
You are a Quality Assurance Editor for a school inspection authority.
Your task is to meticulously review the provided draft inspection report.
Critique the draft based on the following criteria:
1.  **Clarity and Conciseness:** Is the language clear, professional, and free of jargon?
2.  **Objectivity:** Is the tone neutral and based purely on the evidence presented?
3.  **Accuracy:** Does the report accurately reflect the evaluated findings?
4.  **Compliance:** Does the report structure and language align with the official standards of the UAE School Inspection Framework?

Draft Report to Critique:
{draft_report}

Provide your critique as a bulleted list of specific, actionable feedback.
""",
    description="Critiques the draft report for quality, clarity, and compliance.",
    output_key="report_critique"
)

# This agent ONLY produces the final text.
text_refinement_agent = LlmAgent(
    name="TextRefinementAgent",
    model=settings.TEXT_MODEL,
    instruction="""
You are the final editor for the school inspection report.
Your task is to produce the final, polished version of the report's text by incorporating the feedback from the Quality Assurance Editor into the original draft.
Carefully review the original draft and the critique, and apply all necessary revisions.

Original Draft Report:
{draft_report}

Critique and Feedback:
{report_critique}

Output ONLY the complete and polished report in Markdown format.
""",
    description="Produces the final, polished text of the inspection report.",
    output_key="final_report_text"
)