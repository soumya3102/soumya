# main.py
from agents.orchestrator import OrchestratorAgent

def simulate_sankalp_sarathi_demo():
    """Runs a single demonstration session."""
    
    # Must match a key in utils/memory.py for the Memory Bank
    user_id = "DINESH_KUMAR_BIH75K" 
    
    user_query = "My crop has failed. I am a farmer in Bihar. Is any government help available?"

    orchestrator = OrchestratorAgent(user_id)
    
    final_output = orchestrator.run_sankalp_sarathi(user_query)
    
    print("\n=======================================================")
    print("                FINAL APPLICATION GUIDE")
    print("=======================================================")
    print(final_output)

if __name__ == "__main__":
    simulate_sankalp_sarathi_demo()