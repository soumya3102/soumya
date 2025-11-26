# agents/orchestrator.py
from utils.memory import InMemorySessionService
from agents.eligibility_agent import EligibilityAgent
from agents.document_agent import DocumentAgent

class OrchestratorAgent:
    """The Guide: Manages the conversation flow and delegates tasks sequentially."""
    def __init__(self, user_id: str):
        self.session_service = InMemorySessionService(user_id)
        self.eligibility_agent = EligibilityAgent(self.session_service)
        self.document_agent = DocumentAgent(self.session_service)

    def run_sankalp_sarathi(self, user_query: str) -> str:
        """Runs the complete multi-agent workflow."""
        
        profile = self.session_service.get_profile()
        print(f"\n--- 🗣️ Orchestrator Agent: Session Start (User: {profile['name']}) ---")
        print(f"-> [Orchestrator] Original Query: {user_query}")
        
        # 1. Delegation to Eligibility Agent (Gemini Pro)
        print("\n--- 🧠 Step 1: Eligibility Analysis ---")
        eligible_schemes = self.eligibility_agent.determine_eligibility(user_query)
        
        if not eligible_schemes:
            return "I apologize, but no schemes matched your profile and query."

        # 2. Delegation to Document Agent (Gemini Flash)
        print("\n--- 📝 Step 2: Document Generation ---")
        final_guide = self.document_agent.finalize_application_guide(self.session_service)

        print("\n--- 🏁 Orchestrator Agent: Session End ---")
        return final_guide