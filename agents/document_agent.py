# agents/document_agent.py
from google.genai import types
from config import GEMINI_CLIENT, ORCHESTRATOR_MODEL
from utils.memory import InMemorySessionService
import json

class DocumentAgent:
    """The Preparer: Generates the final guide using analysis and simulated built-in tools (Google Search)."""
    def __init__(self, session_service: InMemorySessionService):
        self.client = GEMINI_CLIENT
        self.model = ORCHESTRATOR_MODEL

    def finalize_application_guide(self, session_service):
        schemes = session_service.get_session("eligible_schemes")
        profile = session_service.get_profile()
        
        print("-> [Document Agent] Preparing final checklist and links...")

        if not schemes:
            return "❌ No government schemes were found for your profile and query."

        # Simulate Built-in Tool Search (Google Search) - Using the search terms
        search_terms = " and ".join([s.get('search_term', s['name']) for s in schemes])
        
        # Simulate A2A Protocol for Digital Locker Check
        a2a_status = (
            f"✅ **A2A Protocol Status:** Digital Locker check is complete. "
            f"Your Aadhar Card and Land Records are pre-verified and ready for submission."
            if profile.get("has_digital_locker_aadhar") else 
            "⚠️ A2A Protocol Status: Please be ready to upload physical documents."
        )

        prompt = f"""
        You are the Application Guide. Your task is to create a clear, step-by-step
        guide for the user to apply for the following schemes, formatted in Markdown.

        SCHEME DETAILS (JSON): {json.dumps(schemes, indent=2)}
        A2A PROTOCOL STATUS: {a2a_status}

        Your output must be a single, well-formatted Markdown response in the user's preferred language ({profile['query_language']}).
        
        1. **Summary:** A one-sentence summary of the help available.
        2. **Personalized Checklist:** Combine the documents required by all schemes into a single, comprehensive list.
        3. **Application Links (Simulated Google Search):** Generate simulated official application links for '{search_terms}'.
        4. **A2A Status:** Include the A2A status text provided above.
        """

        response = self.client.models.generate_content(
            model=self.model,
            contents=[types.Content(role="user", parts=[types.Part.from_text(prompt)])]
        )
        
        print("<- [Document Agent] Guide created.")
        return response.text