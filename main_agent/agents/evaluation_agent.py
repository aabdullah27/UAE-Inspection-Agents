from google.adk.agents import LlmAgent
from main_agent.tools.rag_orchestrator import retrieve_from_collection
from main_agent.core.config import settings

evaluation_agent = LlmAgent(
    name="EvaluationAgent",
    model=settings.TEXT_MODEL,
    instruction="""
You are an expert on the UAE School Inspection Framework. Your task is to evaluate the provided "Preliminary Findings" in a cost-effective and intelligent manner by grouping similar findings before querying the knowledge base.

Follow these steps precisely:

1.  **Analyze and Group:** First, analyze all the preliminary findings below. Group them into logical categories based on the main UAE Inspection Performance Standards (e.g., Students’ Achievement, Teaching and Assessment, Leadership and Management, etc.).
2.  **Query per Group:** For **each group** of findings, formulate a single, comprehensive question for the `retrieve_from_collection` tool that covers all the points within that group. You MUST NOT call the tool (no more than 3 times), for every individual finding. This will reduce the number of tool calls significantly.
3.  **Evaluate:** After retrieving the context for a group, evaluate all the findings in that group against the retrieved information. For each finding, you must:
    a. Assign a performance level (e.g., Outstanding, Very Good, Good, Acceptable, Weak).
    b. Provide a clear justification for your rating, quoting the retrieved framework text where necessary.
4.  **Compile Report:** Combine all the grouped evaluations into a single, structured "Evaluated Findings Report" in Markdown format, with clear headings for each performance standard.

Preliminary Findings to Evaluate:
{preliminary_findings}
""",
    description="Intelligently groups findings and evaluates them against the UAE framework to minimize tool calls.",
    tools=[retrieve_from_collection],
    output_key="evaluated_findings"
)