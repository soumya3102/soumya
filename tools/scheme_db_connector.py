# tools/scheme_db_connector.py
import json
import os

class SchemeDBConnector:
    """CUSTOM TOOL: Simulates a query against the Vector Database (RAG)."""
    def __init__(self, data_path='data/gov_schemes_simulated.json'):
        # Correctly resolve the path to the data file
        self.data_path = os.path.join(os.path.dirname(__file__), '..', data_path)
        self.scheme_data = self._load_data()

    def _load_data(self):
        # Handle case where file might not exist yet
        if not os.path.exists(self.data_path):
            return []
        with open(self.data_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def query_scheme_db(self, query_topic: str) -> list[dict]:
        """Tool function: Retrieves schemes based on the query topic."""
        print(f"    [Tool Call] Searching Scheme DB for topic: '{query_topic}'...")
        
        # Simple keyword matching simulation for RAG retrieval
        relevant_schemes = [
            s for s in self.scheme_data 
            if "farmer" in query_topic.lower() or "crop" in query_topic.lower() or "fasal" in query_topic.lower()
        ]
        
        return relevant_schemes

# The function declaration used by the Eligibility Agent
scheme_db_connector_declaration = SchemeDBConnector().query_scheme_db