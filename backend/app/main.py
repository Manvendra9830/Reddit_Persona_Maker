from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .reddit import RedditScraper
from .persona import PersonaAnalyzer, UserPersona

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:3000",  # Local frontend development
    "https://*.vercel.app",   # Production frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    username: str

@app.post("/analyze")
async def analyze_user(request: AnalyzeRequest):
    """
    Analyzes a Reddit user's public activity to generate a persona.
    """
    scraper = RedditScraper()
    analyzer = PersonaAnalyzer()

    try:
        posts, comments = scraper.get_user_content(request.username)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to scrape Reddit content: {e}")

    if not posts and not comments:
        return {
            "username": request.username,
            "has_activity": False,
            "message": "This user has no public posts or comments available for analysis."
        }

    try:
        persona = analyzer.analyze_content(posts, comments)
        persona.username = request.username
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze content with LLM: {e}")

    return {
        "username": persona.username,
        "has_activity": True,
        "persona": {
            "summary": f"A {persona.age or 'unknown age'} {persona.occupation or 'unknown occupation'} who is an {persona.archetype or 'unknown archetype'}.",
            "traits": [
                f"Introvert/Extrovert: {persona.introvert_extrovert}/10",
                f"Intuition/Sensing: {persona.intuition_sensing}/10",
                f"Feeling/Thinking: {persona.feeling_thinking}/10",
                f"Perceiving/Judging: {persona.perceiving_judging}/10",
            ],
            "interests": persona.behavior_habits,
            "motivations": [
                f"Convenience: {persona.convenience}/10",
                f"Wellness: {persona.wellness}/10",
                f"Speed: {persona.speed}/10",
                f"Preferences: {persona.preferences}/10",
                f"Comfort: {persona.comfort}/10",
                f"Dietary Needs: {persona.dietary_needs}/10",
            ],
            "frustrations": persona.frustrations,
            "key_quote": persona.key_quote,
        }
    }