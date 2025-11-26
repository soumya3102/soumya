# config.py
import os
from dotenv import load_dotenv
# Make sure to install the google-genai library: pip install google-genai
from google import genai

load_dotenv() 

ORCHESTRATOR_MODEL = "gemini-2.5-flash"
ELIGIBILITY_MODEL = "gemini-2.5-pro"    # Pro for complex reasoning

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set or is empty.")

GEMINI_CLIENT = genai.Client(api_key=GEMINI_API_KEY)
