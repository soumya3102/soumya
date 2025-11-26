# agents/eligibility_agent.py
import json
from google.genai import types
from config import GEMINI_CLIENT, ELIGIBILITY_MODEL
from tools.scheme_db_connector import SchemeDBConnector
from utils.context_engine import context_compaction

class EligibilityAgent:
    """The Analyst: Determines eligibility using Custom Tool and Gemini Pro."""
    def __init__(self, session_service):
        self.client = GEMINI_CLIENT
        self.model = ELIGIBILITY_MODEL
        self.session_service = session_service
        self.scheme_db = SchemeDBConnector() # Instantiate the Custom Tool

    def determine_eligibility(self, query: str):
        profile = self.session_service.get_profile()
        print(f"-> [Eligibility Agent] Starting analysis for {profile['name']}...")

        # 1. Custom Tool Call (RAG Retrieval)
        retrieved_schemes = self.scheme_db.query_scheme_db(query)

        # 2. Context Compaction
        compacted_context = context_compaction(profile, retrieved_schemes)
        
        # 3. Reasoning with Gemini Pro

        # Define the system instruction and user prompt before the API call
        system_prompt = f"""
        You are the Eligibility Analyst. Match the user's profile and query against the SCHEME DATA.
        
        USER PROFILE: {json.dumps(profile)}
        
        RULES:
        1. Compare the USER PROFILE against the 'Mandatory Eligibility Criteria' in the SCHEME DATA.
        2. Output ONLY the list of schemes the user is 100% eligible for.
        3. Output the result as a strict JSON list of objects, using the schema:
           [{{\"name\": str, \"id\": str, \"documents\": list[str], \"search_term\": str}}]
        """

        user_prompt_text = f"User Query: {query}\n\nSCHEME DATA:\n{compacted_context}"

        response = self.client.models.generate_content(
            model=self.model,
            contents=[
                types.Content(
                    role="user", 
                    parts=[
                        types.Part(text=user_prompt_text)
                    ]
                )
            ],
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json"
            )
        )
        
        try:
            eligible_schemes = json.loads(response.text)
            self.session_service.update_session("eligible_schemes", eligible_schemes)
            print(f"<- [Eligibility Agent] Found {len(eligible_schemes)} eligible schemes.")
            return eligible_schemes
        except json.JSONDecodeError as e:
            print(f"<- [Eligibility Agent] Error parsing JSON output: {e}")
            return []
