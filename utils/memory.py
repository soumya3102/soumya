# utils/memory.py
class InMemorySessionService:
    """Manages active user session data and the Long Term Memory Bank (user profile)."""
    
    USER_PROFILES = {
        "DINESH_KUMAR_BIH75K": {
            "name": "Dinesh Kumar",
            "state": "Bihar",
            "occupation": "Farmer",
            "annual_income": 70000,
            "has_digital_locker_aadhar": True,
            "query_language": "Hindi"
        }
    }

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.session_data = {
            "user_profile": self.USER_PROFILES.get(user_id, {}),
            "eligible_schemes": []
        }
    
    def get_profile(self):
        return self.session_data["user_profile"]

    def update_session(self, key: str, value):
        self.session_data[key] = value

    def get_session(self, key: str):
        return self.session_data.get(key)
