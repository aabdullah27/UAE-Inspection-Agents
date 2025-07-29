# main_agent/tools/pdf_generator.py
import os
import markdown
from xhtml2pdf import pisa
from datetime import datetime
from typing import Dict

# Define the output directory for reports
OUTPUT_DIR = "output_reports"

def create_pdf_report(report_markdown_content: str) -> Dict[str, str]:
    """
    Converts a given Markdown formatted report into a styled PDF file.

    The tool first converts the Markdown to HTML, adds basic styling for a
    professional look, and then renders it as a PDF. The PDF is saved
    locally in the 'output_reports' directory with a unique timestamped name.

    Args:
        report_markdown_content: A string containing the full report in Markdown format.

    Returns:
        A dictionary containing the path to the generated PDF file.
        e.g., {"pdf_file_path": "output_reports/Inspection_Report_20240727_153000.pdf"}
    """
    try:
        # Ensure the output directory exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # Convert Markdown to HTML
        html_content = markdown.markdown(report_markdown_content)

        # Add some basic CSS for styling
        styled_html = f"""
        <html>
        <head>
            <style>
                @page {{
                    size: a4 portrait;
                    @frame content_frame {{
                        left: 50pt; right: 50pt; top: 50pt; bottom: 50pt;
                    }}
                }}
                body {{
                    font-family: 'Helvetica', 'Arial', sans-serif;
                    font-size: 11pt;
                    line-height: 1.5;
                }}
                h1 {{
                    font-size: 24pt;
                    color: #333;
                    border-bottom: 2px solid #ccc;
                    padding-bottom: 10px;
                    margin-bottom: 20px;
                }}
                h2 {{
                    font-size: 18pt;
                    color: #444;
                    margin-top: 25px;
                    border-bottom: 1px solid #eee;
                    padding-bottom: 5px;
                }}
                h3 {{
                    font-size: 14pt;
                    color: #555;
                }}
                p {{
                    margin-bottom: 12px;
                }}
                ul {{
                    padding-left: 20pt;
                }}
                li {{
                    margin-bottom: 8px;
                }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """

        # Generate a unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"Inspection_Report_{timestamp}.pdf"
        file_path = os.path.join(OUTPUT_DIR, file_name)

        # Create the PDF
        with open(file_path, "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(styled_html, dest=pdf_file)

        if pisa_status.err:
            error_message = f"PDF generation failed with error code {pisa_status.err}"
            return {"error": error_message}

        return {"pdf_file_path": file_path}

    except Exception as e:
        return {"error": f"An unexpected error occurred during PDF generation: {str(e)}"}