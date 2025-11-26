# utils/context_engine.py
import json

def context_compaction(user_profile: dict, retrieved_schemes: list[dict]) -> str:
    """
    Context Compaction: Filters and formats raw scheme data for LLM analysis.
    This reduces the token count passed to Gemini Pro.
    """
    compacted_data = []
    
    for scheme in retrieved_schemes:
        is_relevant = True
        
        # Simple Relevance Check based on State
        if scheme["state"] != "Central" and scheme["state"] != user_profile.get("state"):
            is_relevant = False
        
        if is_relevant:
            compacted_data.append({
                "Scheme Name": scheme["name"],
                "Focus": scheme["focus"],
                "Applicable State": scheme["state"],
                "Mandatory Eligibility Criteria": scheme["criteria"],
                "Required Documents": scheme["documents"],
                "search_term": scheme["link_search_term"] # Pass this for later use
            })

    if not compacted_data:
        return "No schemes found relevant to the user's profile."

    return json.dumps(compacted_data, indent=2)
