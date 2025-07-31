# streamlit_app.py
import streamlit as st
import asyncio
import os
import uuid
from typing import Any, Dict
import sys, pathlib; sys.path.extend(
    str(p) for p in {
        pathlib.Path(__file__).resolve().parent.parent,
        pathlib.Path(__file__).resolve().parent.parent / 'main_agent',
    } if str(p) not in sys.path
)
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import pymupdf4llm

# Import the root agent from your project structure
from main_agent.agent import root_agent

# --- Configuration ---
APP_NAME = "school_inspection_app"
USER_ID = "streamlit_user"
TEMP_DATA_DIR = "temp_data"

# --- ADK Runner and Session Management ---

@st.cache_resource
def get_adk_runner() -> Runner:
    """Initializes and caches the ADK Runner for the Streamlit session."""
    print("Initializing ADK Runner...")
    session_service = InMemorySessionService()
    return Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

async def get_or_create_session(runner: Runner, session_id: str) -> None:
    """Ensures a session exists for the given ID."""
    session = await runner.session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=session_id
    )
    if not session:
        await runner.session_service.create_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=session_id, state={}
        )
        print(f"Created new ADK session: {session_id}")

# --- Main Application Logic ---

async def run_inspection_pipeline(
    pdf_path: str, session_id: str
) -> None:
    """
    Runs the full inspection pipeline and updates the UI with results.
    """
    runner = get_adk_runner()
    await get_or_create_session(runner, session_id)

    # Reset state for the new run
    st.session_state.results = {}
    st.session_state.pdf_path = None
    st.session_state.error = None

    try:
        # 1. Read and prepare textual evidence from the uploaded PDF
        with st.session_state.placeholders["status"]:
            st.info("Step 1: Extracting text from the uploaded PDF...")
        textual_evidence = pymupdf4llm.to_markdown(pdf_path, write_images=False)
        if not textual_evidence:
            st.session_state.error = "Could not extract any text from the PDF. Please try another file."
            with st.session_state.placeholders["status"]:
                st.error(st.session_state.error)
            return

        initial_state = {
            "textual_evidence": textual_evidence,
            "video_evidence_uri": "",
            "audio_evidence_transcript": ""
        }
        
        with st.session_state.placeholders["status"]:
            st.info("Step 2: Running the multi-agent analysis pipeline...")

        # 2. Run the ADK pipeline
        events_async = runner.run_async(
            user_id=USER_ID,
            session_id=session_id,
            new_message=types.Content(
                role="user",
                parts=[types.Part(text="Start the inspection process for the provided evidence.")],
            ),
            state_delta=initial_state
        )

        # 3. Process events and display results as they become available
        async for event in events_async:
            author = event.author
            
            # Display final text responses from agents
            if event.is_final_response() and event.content and event.content.parts:
                response_text = event.content.parts[0].text
                if response_text and author and author in st.session_state.placeholders:
                    st.session_state.results[author] = response_text
                    with st.session_state.placeholders[author]:
                        with st.expander(f"✅ Output from: **{author}**", expanded=True):
                            st.markdown(response_text)

            # Capture the generated PDF path from the tool's response
            if event.content and event.content.parts and event.content.parts[0].function_response:
                func_response = event.content.parts[0].function_response
                if func_response.name == "create_pdf_report":
                    response_data = func_response.response
                    if isinstance(response_data, dict) and "pdf_file_path" in response_data:
                        st.session_state.pdf_path = response_data["pdf_file_path"]

        with st.session_state.placeholders["status"]:
            st.success("Pipeline finished successfully!")


    except Exception as e:
        st.session_state.error = f"An error occurred during the inspection pipeline: {e}"
        with st.session_state.placeholders["status"]:
             st.error(st.session_state.error)
        print(f"Error: {e}")


def main():
    """Defines the Streamlit UI."""
    st.set_page_config(page_title="UAE School Inspection Assistant", layout="wide")
    st.title("🏫 UAE School Inspection Report Generator")
    st.markdown(
        "Upload a PDF with inspection evidence (e.g., lesson plans, observation notes). "
        "The AI pipeline will analyze it, evaluate it against the UAE framework, and generate a formal report."
    )
    
    # Initialize session state
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "results" not in st.session_state:
        st.session_state.results = {}
    if "pdf_path" not in st.session_state:
        st.session_state.pdf_path = None
    if "placeholders" not in st.session_state:
         st.session_state.placeholders = {}
    if "error" not in st.session_state:
         st.session_state.error = None


    # File Uploader
    uploaded_file = st.file_uploader(
        "Upload Inspection Evidence PDF", type="pdf", key="file_uploader"
    )

    if uploaded_file:
        if st.button("Start Inspection and Generate Report", type="primary"):
            # Clean up state from previous runs
            st.session_state.results = {}
            st.session_state.pdf_path = None
            st.session_state.error = None
            
            # Save the uploaded file to a temporary location
            os.makedirs(TEMP_DATA_DIR, exist_ok=True)
            file_path = os.path.join(TEMP_DATA_DIR, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.success(f"File '{uploaded_file.name}' uploaded and ready for processing.")
            st.divider()

            # --- Vertically oriented UI for pipeline results ---
            st.header("Inspection Pipeline Progress")
            
            # Define the order of agents for display
            agent_names_in_order = [
                "status", # For general status updates
                "TextAnalysisAgent",
                "SynthesisAgent",
                "FinalReportAgent"
            ]
            
            # Create vertical placeholders
            for name in agent_names_in_order:
                st.session_state.placeholders[name] = st.empty()
            
            # Run the asynchronous pipeline
            asyncio.run(run_inspection_pipeline(file_path, st.session_state.session_id))

    # Display Download Button at the end if PDF is ready
    if st.session_state.get("pdf_path") and os.path.exists(st.session_state.pdf_path):
        st.divider()
        st.header("Download Your Report")
        with open(st.session_state.pdf_path, "rb") as pdf_file:
            st.download_button(
                label="Download Inspection Report (PDF)",
                data=pdf_file,
                file_name=os.path.basename(st.session_state.pdf_path),
                mime="application/pdf",
                type="primary",
                key="download_button"
            )

if __name__ == "__main__":
    main()