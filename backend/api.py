import sys
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re
from groq import Groq # Add Groq import for warm-up call

# Add the directory containing this script to the sys.path
# This allows importing reddit_persona_generator
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the persona generation logic from the existing script
from reddit_persona_generator import generate_persona

app = FastAPI()

# CORS configuration to allow frontend requests from Vercel and localhost
# FastAPI does not support wildcard domains in `allow_origins`, so we use a regex.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (POST, GET, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

# D) Cold Start Warm-up Strategy
@app.on_event("startup")
def startup_event():
    print("API Startup: Running cold start warm-up...")
    try:
        # Initialize Groq client (requires GROQ_API_KEY from env)
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        # Perform a harmless, cached LLM call with fixed text
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": "hello"}
            ],
            model="llama-3.1-8b-instant", # Using a common, fast Groq model for warm-up
            temperature=0.1, # Low temperature for consistent, fast response
            max_tokens=10, # Keep response very short
        )
        print(f"API Warm-up successful: {chat_completion.choices[0].message.content}")
    except Exception as e:
        print(f"API Warm-up failed: {e}")
    print("API Startup: Cold start warm-up complete.")

class AnalyzeRequest(BaseModel):
    username: str

@app.post("/analyze")
def analyze_user(request: AnalyzeRequest):
    """
    Analyzes a Reddit user's public activity to generate a persona.
    This endpoint calls the underlying logic from the persona generator script.
    """
    # Sanitize username
    username = re.sub(r"^/?u/", "", request.username)
    model_name = "llama-3.1-8b-instant" # Using a fixed, known-good model for the API

    try:
        result = generate_persona(username, model_name)
        
        if not result["has_activity"]:
            return {
                "username": username,
                "has_activity": False,
                "message": result["message"]
            }

        # The API should return the JSON-serializable dictionary
        return {
            "username": username,
            "has_activity": True,
            "persona": result["persona_dict"]
        }

    except Exception as e:
        # Catch any unexpected errors from the script and return a 500 error
        raise HTTPException(status_code=500, detail=str(e))
