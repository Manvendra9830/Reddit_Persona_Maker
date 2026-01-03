import sys
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re

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
