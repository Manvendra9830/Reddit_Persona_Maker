#!/usr/bin/env python3
"""
Reddit User Persona Generator

This script scrapes a Reddit user's profile, analyzes their posts and comments,
and generates a comprehensive user persona with citations.

Requirements:
- praw (Python Reddit API Wrapper)
- ollama (for LLM analysis)
- python-dotenv (for environment variables)

Usage:
    python reddit_persona_generator.py <reddit_username>

Install Ollama models:
    ollama pull mistral
    ollama pull llama3.2

cmd for giving powershell permission to make and activate the virtual environment
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
"""

import os
import sys
import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from dotenv import load_dotenv

import praw
import requests
import ollama

# Load environment variables
load_dotenv()


@dataclass
class Citation:
    """Represents a citation for a piece of information."""

    post_id: str
    post_type: str  # 'post' or 'comment'
    content: str
    subreddit: str
    timestamp: str
    url: str


@dataclass
class UserPersona:
    """Represents a complete user persona."""

    username: str
    age: Optional[str] = None
    occupation: Optional[str] = None
    status: Optional[str] = None
    location: Optional[str] = None
    tier: Optional[str] = None
    archetype: Optional[str] = None

    # Personality traits (scale values)
    introvert_extrovert: Optional[int] = None  # 1-10 scale
    intuition_sensing: Optional[int] = None
    feeling_thinking: Optional[int] = None
    perceiving_judging: Optional[int] = None

    # Motivations (scale values 1-10)
    convenience: Optional[int] = None
    wellness: Optional[int] = None
    speed: Optional[int] = None
    preferences: Optional[int] = None
    comfort: Optional[int] = None
    dietary_needs: Optional[int] = None

    # Behavioral patterns
    behavior_habits: List[str] = None
    frustrations: List[str] = None
    goals_needs: List[str] = None

    # Key quote
    key_quote: Optional[str] = None

    # Citations for each field
    citations: Dict[str, List[Citation]] = None

    def __post_init__(self):
        if self.behavior_habits is None:
            self.behavior_habits = []
        if self.frustrations is None:
            self.frustrations = []
        if self.goals_needs is None:
            self.goals_needs = []
        if self.citations is None:
            self.citations = {}


class RedditScraper:
    """Handles Reddit API interactions and data scraping."""

    def __init__(self):
        """Initialize Reddit API client."""
        self.reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT", "PersonaGenerator/1.0"),
        )

    def get_user_content(
        self, username: str, limit: int = 100
    ) -> Tuple[List[Dict], List[Dict]]:
        """
        Scrape user's posts and comments.

        Args:
            username: Reddit username
            limit: Maximum number of items to scrape

        Returns:
            Tuple of (posts, comments)
        """
        try:
            user = self.reddit.redditor(username)

            # Get posts
            posts = []
            for submission in user.submissions.new(limit=limit):
                posts.append(
                    {
                        "id": submission.id,
                        "title": submission.title,
                        "content": submission.selftext,
                        "subreddit": str(submission.subreddit),
                        "score": submission.score,
                        "created_utc": submission.created_utc,
                        "url": f"https://reddit.com{submission.permalink}",
                        "type": "post",
                    }
                )

            # Get comments
            comments = []
            for comment in user.comments.new(limit=limit):
                comments.append(
                    {
                        "id": comment.id,
                        "content": comment.body,
                        "subreddit": str(comment.subreddit),
                        "score": comment.score,
                        "created_utc": comment.created_utc,
                        "url": f"https://reddit.com{comment.permalink}",
                        "type": "comment",
                    }
                )

            return posts, comments

        except Exception as e:
            print(f"Error scraping user {username}: {e}")
            return [], []


class PersonaAnalyzer:
    """Analyzes Reddit content to generate user personas using Ollama LLM."""

    def __init__(self, model_name: str = "mistral"):
        """Initialize Ollama client."""
        self.model_name = model_name

        # Test if Ollama is running and model is available
        try:
            response = ollama.list()
            available_models = [model["name"] for model in response["models"]]
            if self.model_name not in available_models:
                print(
                    f"Warning: Model '{self.model_name}' not found. Available models: {available_models}"
                )
                print(f"Please run: ollama pull {self.model_name}")
        except Exception as e:
            print(f"Error connecting to Ollama: {e}")
            print("Make sure Ollama is running. Start it with: ollama serve")

    def analyze_content(self, posts: List[Dict], comments: List[Dict]) -> UserPersona:
        """
        Analyze posts and comments to generate persona.

        Args:
            posts: List of user posts
            comments: List of user comments

        Returns:
            UserPersona object
        """
        # Combine all content
        all_content = posts + comments

        # Create analysis prompt
        content_text = self._format_content_for_analysis(all_content)

        # Truncate content if too long (Ollama has context limits)
        if len(content_text) > 8000:
            content_text = content_text[:8000] + "\n... (content truncated)"

        prompt = f"""
        Analyze the following Reddit posts and comments to create a detailed user persona. 
        Based on the content, extract information about:

        1. Demographics (age, occupation, location, relationship status)
        2. Personality traits on scales of 1-10:
           - Introvert (1) vs Extrovert (10)
           - Intuition (1) vs Sensing (10)
           - Feeling (1) vs Thinking (10)
           - Perceiving (1) vs Judging (10)
        3. Motivations (rate 1-10): convenience, wellness, speed, preferences, comfort, dietary_needs
        4. Behavioral patterns and habits
        5. Frustrations and pain points
        6. Goals and needs
        7. A key quote that represents the user (pick from their actual content)
        8. User archetype (e.g., "The Creator", "The Explorer", "The Caregiver")
        9. User tier (e.g., "Early Adopter", "Mainstream", "Laggard")

        For each characteristic (like age, occupation, frustrations, etc), you MUST list the exact post/comment IDs used from the provided content. 
        DO NOT guess or leave them empty unless absolutely no supporting content exists.
        Ensure the 'citations' field is present and includes at least one matching ID for each non-empty characteristic.



        Content to analyze:
        {content_text}

        IMPORTANT: Respond ONLY in valid JSON format with the following structure:
        {{
            "demographics": {{
                "age": "estimated age range",
                "occupation": "likely occupation",
                "location": "location if mentioned",
                "status": "relationship status",
                "tier": "user tier",
                "archetype": "user archetype"
            }},
            "personality": {{
                "introvert_extrovert": 5,
                "intuition_sensing": 5,
                "feeling_thinking": 5,
                "perceiving_judging": 5
            }},
            "motivations": {{
                "convenience": 5,
                "wellness": 5,
                "speed": 5,
                "preferences": 5,
                "comfort": 5,
                "dietary_needs": 5
            }},
            "behavior_habits": ["habit 1", "habit 2"],
            "frustrations": ["frustration 1", "frustration 2"],
            "goals_needs": ["goal 1", "goal 2"],
            "key_quote": "representative quote from their content",
            "citations": {{
                "age": ["post_id_1", "comment_id_2"],
                "occupation": ["post_id_3"],
                "location": ["comment_id_4"],
                "status": ["post_id_5"],
                "tier": ["comment_id_6"],
                "archetype": ["post_id_7"],
                "behavior_habits": ["post_id_8"],
                "frustrations": ["comment_id_9"],
                "goals_needs": ["post_id_10"],
                "key_quote": ["comment_id_11"]
            }}
        }}
        """

        try:
            response = self._get_ollama_response(prompt)

            # Clean up the response to extract JSON
            response = self._clean_json_response(response)
            analysis = json.loads(response)

            return self._create_persona_from_analysis(analysis, all_content)

        except Exception as e:
            print(f"Error analyzing content: {e}")
            print(
                f"Raw response: {response if 'response' in locals() else 'No response'}"
            )
            return UserPersona(username="unknown")

    def _format_content_for_analysis(self, content: List[Dict]) -> str:
        """Format content for LLM analysis."""
        formatted = []
        for item in content:
            timestamp = datetime.fromtimestamp(item["created_utc"]).strftime("%Y-%m-%d")
            if item["type"] == "post":
                formatted.append(
                    f"[POST {item['id']}] [{timestamp}] r/{item['subreddit']}: {item['title']}"
                )
                if item["content"]:
                    formatted.append(f"Content: {item['content'][:500]}...")
            else:
                formatted.append(
                    f"[COMMENT {item['id']}] [{timestamp}] r/{item['subreddit']}: {item['content'][:500]}..."
                )
            formatted.append("")

        return "\n".join(formatted)

    def _get_ollama_response(self, prompt: str) -> str:
        """Get response from Ollama."""
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.7, "top_p": 0.9, "max_tokens": 4096},
            )
            return response["message"]["content"]
        except Exception as e:
            print(f"Error getting Ollama response: {e}")
            raise

    def _clean_json_response(self, response: str) -> str:
        """Clean up the response to extract valid JSON."""
        # Remove markdown formatting
        response = re.sub(r"```json\s*", "", response)
        response = re.sub(r"```\s*$", "", response)

        # Fix invalid values
        response = re.sub(
            r"(:\s*)(Not mentioned|Not specified|None)(\s*[,\}])", r': "\2"\3', response
        )

        # Truncate at first valid JSON object (if multiple or incomplete)
        stack = []
        start = None
        for i, char in enumerate(response):
            if char == "{":
                if not stack:
                    start = i
                stack.append("{")
            elif char == "}":
                stack.pop()
                if not stack and start is not None:
                    response = response[start : i + 1]
                    break

        return response

    def _create_persona_from_analysis(
        self, analysis: Dict, content: List[Dict]
    ) -> UserPersona:
        """Create UserPersona object from analysis results."""
        # Create content lookup
        content_lookup = {item["id"]: item for item in content}

        # Extract demographics
        demographics = analysis.get("demographics", {})
        personality = analysis.get("personality", {})
        motivations = analysis.get("motivations", {})

        # Create persona
        persona = UserPersona(
            username=content[0].get("username", "unknown") if content else "unknown",
            age=demographics.get("age"),
            occupation=demographics.get("occupation"),
            status=demographics.get("status"),
            location=demographics.get("location"),
            tier=demographics.get("tier"),
            archetype=demographics.get("archetype"),
            # Personality traits
            introvert_extrovert=personality.get("introvert_extrovert"),
            intuition_sensing=personality.get("intuition_sensing"),
            feeling_thinking=personality.get("feeling_thinking"),
            perceiving_judging=personality.get("perceiving_judging"),
            # Motivations
            convenience=motivations.get("convenience"),
            wellness=motivations.get("wellness"),
            speed=motivations.get("speed"),
            preferences=motivations.get("preferences"),
            comfort=motivations.get("comfort"),
            dietary_needs=motivations.get("dietary_needs"),
            # Lists
            behavior_habits=analysis.get("behavior_habits", []),
            frustrations=analysis.get("frustrations", []),
            goals_needs=analysis.get("goals_needs", []),
            key_quote=analysis.get("key_quote"),
        )

        # Create citations
        citations = {}
        citation_data = analysis.get("citations", {})

        for field, cited_ids in citation_data.items():
            citations[field] = []
            for cited_id in cited_ids:
                if cited_id in content_lookup:
                    item = content_lookup[cited_id]
                    citation = Citation(
                        post_id=cited_id,
                        post_type=item["type"],
                        content=item.get("content", item.get("title", ""))[:200]
                        + "...",
                        subreddit=item["subreddit"],
                        timestamp=datetime.fromtimestamp(item["created_utc"]).strftime(
                            "%Y-%m-%d"
                        ),
                        url=item["url"],
                    )
                    citations[field].append(citation)

        persona.citations = citations
        return persona


class PersonaFormatter:
    """Formats persona data for output."""

    @staticmethod
    def format_persona_to_text(persona: UserPersona) -> str:
        """Format persona as human-readable text with citations."""
        output = []

        # Header
        output.append("=" * 60)
        output.append(f"USER PERSONA: {persona.username.upper()}")
        output.append("=" * 60)
        output.append("")

        # Demographics
        output.append("DEMOGRAPHICS")
        output.append("-" * 20)
        if persona.age:
            output.append(f"Age: {persona.age}")
            PersonaFormatter._add_citations(output, persona.citations.get("age", []))

        if persona.occupation:
            output.append(f"Occupation: {persona.occupation}")
            PersonaFormatter._add_citations(
                output, persona.citations.get("occupation", [])
            )

        if persona.status:
            output.append(f"Status: {persona.status}")
            PersonaFormatter._add_citations(output, persona.citations.get("status", []))

        if persona.location:
            output.append(f"Location: {persona.location}")
            PersonaFormatter._add_citations(
                output, persona.citations.get("location", [])
            )

        if persona.tier:
            output.append(f"Tier: {persona.tier}")
            PersonaFormatter._add_citations(output, persona.citations.get("tier", []))

        if persona.archetype:
            output.append(f"Archetype: {persona.archetype}")
            PersonaFormatter._add_citations(
                output, persona.citations.get("archetype", [])
            )

        output.append("")

        # Personality
        output.append("PERSONALITY TRAITS")
        output.append("-" * 20)
        if persona.introvert_extrovert:
            trait = "Extrovert" if persona.introvert_extrovert > 5 else "Introvert"
            output.append(
                f"Introvert/Extrovert: {trait} ({persona.introvert_extrovert}/10)"
            )

        if persona.intuition_sensing:
            trait = "Sensing" if persona.intuition_sensing > 5 else "Intuition"
            output.append(
                f"Intuition/Sensing: {trait} ({persona.intuition_sensing}/10)"
            )

        if persona.feeling_thinking:
            trait = "Thinking" if persona.feeling_thinking > 5 else "Feeling"
            output.append(f"Feeling/Thinking: {trait} ({persona.feeling_thinking}/10)")

        if persona.perceiving_judging:
            trait = "Judging" if persona.perceiving_judging > 5 else "Perceiving"
            output.append(
                f"Perceiving/Judging: {trait} ({persona.perceiving_judging}/10)"
            )

        output.append("")

        # Motivations
        output.append("MOTIVATIONS")
        output.append("-" * 20)
        motivations = [
            ("Convenience", persona.convenience),
            ("Wellness", persona.wellness),
            ("Speed", persona.speed),
            ("Preferences", persona.preferences),
            ("Comfort", persona.comfort),
            ("Dietary Needs", persona.dietary_needs),
        ]

        for name, value in motivations:
            if value:
                output.append(f"{name}: {value}/10")

        output.append("")

        # Behaviors & Habits
        if persona.behavior_habits:
            output.append("BEHAVIOR & HABITS")
            output.append("-" * 20)
            for habit in persona.behavior_habits:
                output.append(f"• {habit}")
            PersonaFormatter._add_citations(
                output, persona.citations.get("behavior_habits", [])
            )
            output.append("")

        # Frustrations
        if persona.frustrations:
            output.append("FRUSTRATIONS")
            output.append("-" * 20)
            for frustration in persona.frustrations:
                output.append(f"• {frustration}")
            PersonaFormatter._add_citations(
                output, persona.citations.get("frustrations", [])
            )
            output.append("")

        # Goals & Needs
        if persona.goals_needs:
            output.append("GOALS & NEEDS")
            output.append("-" * 20)
            for goal in persona.goals_needs:
                output.append(f"• {goal}")
            PersonaFormatter._add_citations(
                output, persona.citations.get("goals_needs", [])
            )
            output.append("")

        # Key Quote
        if persona.key_quote:
            output.append("KEY QUOTE")
            output.append("-" * 20)
            output.append(f'"{persona.key_quote}"')
            PersonaFormatter._add_citations(
                output, persona.citations.get("key_quote", [])
            )
            output.append("")

        return "\n".join(output)

    @staticmethod
    def _add_citations(output: List[str], citations: List[Citation]):
        """Add citations to output."""
        if citations:
            output.append("   Citations:")
            for citation in citations:
                output.append(
                    f"   - [{citation.post_type.upper()}] {citation.timestamp} r/{citation.subreddit}"
                )
                output.append(f"     {citation.content}")
                output.append(f"     {citation.url}")
                output.append("")


def main():
    """Main function to run the persona generator."""
    if len(sys.argv) < 2:
        print(
            "Usage: python reddit_persona_generator.py <reddit_username> [model_name]"
        )
        print("Example: python reddit_persona_generator.py kojied mistral")
        print("Example: python reddit_persona_generator.py kojied llama3.2")
        print("Available models: mistral, llama3.2, llama3.1, codellama")
        sys.exit(1)

    username = sys.argv[1]
    model_name = sys.argv[2] if len(sys.argv) > 2 else "mistral"

    # Remove /u/ or u/ prefix if present
    username = re.sub(r"^/?u/", "", username)

    print(f"Generating persona for Reddit user: {username}")
    print(f"Using model: {model_name}")
    print("=" * 50)

    # Initialize components
    scraper = RedditScraper()
    analyzer = PersonaAnalyzer(model_name=model_name)

    # Scrape user content
    print("1. Scraping user posts and comments...")
    posts, comments = scraper.get_user_content(username)

    if not posts and not comments:
        print(f"No content found for user {username}")
        sys.exit(1)

    print(f"   Found {len(posts)} posts and {len(comments)} comments")

    # Analyze content
    print("2. Analyzing content with LLM...")
    persona = analyzer.analyze_content(posts, comments)
    persona.username = username

    # Format and save output
    print("3. Generating persona report...")
    formatted_output = PersonaFormatter.format_persona_to_text(persona)

    # Save to file
    output_filename = f"{username}_persona_{model_name}.txt"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(formatted_output)

    print(f"4. Persona saved to {output_filename}")
    print("\nPersona Summary:")
    print("-" * 30)
    print(f"User: {persona.username}")
    print(f"Age: {persona.age or 'Unknown'}")
    print(f"Occupation: {persona.occupation or 'Unknown'}")
    print(f"Archetype: {persona.archetype or 'Unknown'}")
    if persona.key_quote:
        print(f'Key Quote: "{persona.key_quote}"')


if __name__ == "__main__":
    main()
