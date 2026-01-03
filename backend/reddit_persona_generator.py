#!/usr/bin/env python3
"""
Reddit User Persona Generator (Single-File Backend)

This script scrapes a Reddit user's profile, analyzes their posts and comments
using the Groq LLM, and generates a comprehensive user persona with citations.
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
from groq import Groq

# Load environment variables from .env file
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
        Scrape user's posts and comments with robust filtering.

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
                # Filter out deleted/removed posts and those without meaningful content
                if (
                    submission.selftext
                    and submission.selftext.strip() not in ["[deleted]", "[removed]"]
                    and submission.selftext.strip()
                    and not getattr(submission, 'removed_by_category', False)
                ):
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
                # Filter out deleted/removed comments and those without meaningful content
                if (
                    comment.body
                    and comment.body.strip() not in ["[deleted]", "[removed]"]
                    and comment.body.strip()
                    and comment.author
                ):
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
    """Analyzes Reddit content to generate user personas using Groq LLM."""

    def __init__(self, model_name: str = "llama-3.1-8b-instant"):
        """Initialize Groq client."""
        self.model_name = model_name
        try:
            self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        except Exception as e:
            print(f"Error initializing Groq client: {e}")
            sys.exit(1)

    def analyze_content(self, posts: List[Dict], comments: List[Dict]) -> UserPersona:
        """
        Analyze posts and comments to generate persona.
        """
        all_content = posts + comments
        content_text = self._format_content_for_analysis(all_content)

        if len(content_text) > 8000:
            content_text = content_text[:8000] + "\n... (content truncated)"

        prompt = f"""
        Analyze the following Reddit posts and comments to create a detailed, evidence-based user persona. 
        Your analysis MUST be grounded in the provided text. Do NOT speculate or use phrases like "possibly" or "might be". 
        If evidence for a field is not present, omit the field entirely.

        For EACH characteristic (e.g., age, occupation, a specific habit), you MUST provide citations from the user's content.
        A citation MUST include the `post_id` or `comment_id`.

        Content to analyze:
        {content_text}

                IMPORTANT: Respond ONLY in valid JSON format with the following structure.

                EVERY field in the JSON response that is not empty MUST have a corresponding citation.

                For each citation, include the content snippet (up to 200 characters) from the original Reddit post/comment that directly supports the claim.

        

                {{

                    "demographics": {{"age": "estimated age range", "occupation": "likely occupation", "location": "location if mentioned", "status": "relationship status", "tier": "user tier", "archetype": "user archetype"}},

                    "personality": {{"introvert_extrovert": 5, "intuition_sensing": 5, "feeling_thinking": 5, "perceiving_judging": 5}},

                    "motivations": {{"convenience": 5, "wellness": 5, "speed": 5, "preferences": 5, "comfort": 5, "dietary_needs": 5}},

                    "behavior_habits": ["habit 1", "habit 2"],

                    "frustrations": ["frustration 1", "frustration 2"],

                    "goals_needs": ["goal 1", "goal 2"],

                    "key_quote": "representative quote from their content",

                    "citations": {{

                        "age": [

                            {{"id": "post_id_1", "content_snippet": "Relevant text from post 1 (max 200 chars)"}},

                            {{"id": "comment_id_2", "content_snippet": "Relevant text from comment 2 (max 200 chars)"}}

                        ],

                        "occupation": [

                            {{"id": "post_id_3", "content_snippet": "Relevant text from post 3 (max 200 chars)"}}

                        ],

                        "location": [

                            {{"id": "comment_id_4", "content_snippet": "Relevant text from comment 4 (max 200 chars)"}}

                        ],

                        "status": [

                            {{"id": "post_id_5", "content_snippet": "Relevant text from post 5 (max 200 chars)"}}

                        ],

                        "tier": [

                            {{"id": "comment_id_6", "content_snippet": "Relevant text from comment 6 (max 200 chars)"}}

                        ],

                        "archetype": [

                            {{"id": "post_id_7", "content_snippet": "Relevant text from post 7 (max 200 chars)"}}

                        ],

                        "behavior_habits": [

                            {{"id": "post_id_8", "content_snippet": "Relevant text from post 8 (max 200 chars)"}},

                            {{"id": "comment_id_9", "content_snippet": "Relevant text from comment 9 (max 200 chars)"}}

                        ],

                        "frustrations": [

                            {{"id": "comment_id_10", "content_snippet": "Relevant text from comment 10 (max 200 chars)"}}

                        ],

                        "goals_needs": [

                            {{"id": "post_id_11", "content_snippet": "Relevant text from post 11 (max 200 chars)"}}

                        ],

                        "key_quote": [

                            {{"id": "comment_id_12", "content_snippet": "Relevant text from comment 12 (max 200 chars)"}}

                        ]

                    }}

                }}

                """

        try:
            raw_llm_response = self._get_groq_response(prompt)
            print("DEBUG: Raw LLM Response:", raw_llm_response)
            response = self._clean_json_response(raw_llm_response)
            print("DEBUG: Cleaned JSON Response:", response)
            analysis = json.loads(response)
            return self._create_persona_from_analysis(analysis, all_content)
        except Exception as e:
            print(f"Error analyzing content: {e}")
            print(f"Raw response: {response if 'response' in locals() else 'No response'}")
            return UserPersona(username="unknown")

    def _format_content_for_analysis(self, content: List[Dict]) -> str:
        """Format content for LLM analysis."""
        formatted = []
        for item in content:
            timestamp = datetime.fromtimestamp(item["created_utc"]).strftime("%Y-%m-%d")
            if item["type"] == "post":
                formatted.append(f"[POST {item['id']}] [{timestamp}] r/{item['subreddit']}: {item['title']}")
                if item["content"]:
                    formatted.append(f"Content: {item['content'][:500]}...")
            else:
                formatted.append(f"[COMMENT {item['id']}] [{timestamp}] r/{item['subreddit']}: {item['content'][:500]}...")
            formatted.append("")
        return "\n".join(formatted)

    def _get_groq_response(self, prompt: str) -> str:
        """Get response from Groq LLM."""
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"Error getting Groq response: {e}")
            raise

    def _clean_json_response(self, response: str) -> str:
        """Clean up the response to extract valid JSON."""
        response = re.sub(r"```json\s*", "", response, flags=re.IGNORECASE)
        response = re.sub(r"```\s*$", "", response)

        # Remove single-line JavaScript-style comments (// ...)
        response = re.sub(r"//.*", "", response)

        # Remove trailing commas
        response = re.sub(r",\s*([\}\]])", r"\1", response)

        # Find the first '{' and the last '}' to extract the JSON object
        start = response.find('{')
        end = response.rfind('}')
        if start != -1 and end != -1:
            response = response[start:end+1]
        
        return response

    def _create_persona_from_analysis(self, analysis: Dict, content: List[Dict]) -> UserPersona:
        """Create UserPersona object from analysis results and correctly parse citations."""
        content_lookup = {item["id"]: item for item in content}

        demographics = analysis.get("demographics", {})
        personality = analysis.get("personality", {})
        motivations = analysis.get("motivations", {})

        persona = UserPersona(
            username=content[0].get("username", "unknown") if content else "unknown",
            age=demographics.get("age"),
            occupation=demographics.get("occupation"),
            status=demographics.get("status"),
            location=demographics.get("location"),
            tier=demographics.get("tier"),
            archetype=demographics.get("archetype"),
            introvert_extrovert=personality.get("introvert_extrovert"),
            intuition_sensing=personality.get("intuition_sensing"),
            feeling_thinking=personality.get("feeling_thinking"),
            perceiving_judging=personality.get("perceiving_judging"),
            convenience=motivations.get("convenience"),
            wellness=motivations.get("wellness"),
            speed=motivations.get("speed"),
            preferences=motivations.get("preferences"),
            comfort=motivations.get("comfort"),
            dietary_needs=motivations.get("dietary_needs"),
            behavior_habits=analysis.get("behavior_habits", []),
            frustrations=analysis.get("frustrations", []),
            goals_needs=analysis.get("goals_needs", []),
            key_quote=analysis.get("key_quote"),
        )

        # --- Custom Citation Parsing Logic ---
        persona.citations = {}
        citation_data = analysis.get("citations", {})

        for field, citations_list_from_llm in citation_data.items():
            if isinstance(citations_list_from_llm, list):
                persona.citations[field] = []
                for citation_item in citations_list_from_llm:
                    if isinstance(citation_item, dict) and "id" in citation_item and "content_snippet" in citation_item:
                        actual_id = str(citation_item["id"]).replace("post_id_", "").replace("comment_id_", "")
                        content_snippet = citation_item["content_snippet"]

                        if actual_id in content_lookup:
                            item = content_lookup[actual_id]
                            persona.citations[field].append(Citation(
                                post_id=actual_id,
                                post_type=item["type"],
                                content=content_snippet, # Use the content_snippet provided by the LLM
                                subreddit=item["subreddit"],
                                timestamp=datetime.fromtimestamp(item["created_utc"]).strftime("%Y-%m-%d"),
                                url=item["url"],
                            ))
        # --- End Custom Citation Parsing Logic ---

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
                output.append(f"   - [{citation.post_type.upper()}] {citation.timestamp} r/{citation.subreddit}")
                output.append(f"     {citation.content}")
                output.append(f"     {citation.url}\n")


def main():
    """Main function to run the persona generator."""
    if len(sys.argv) < 2:
        print("Usage: python backend/reddit_persona_generator.py <reddit_username> [model_name]")
        print("Example: python backend/reddit_persona_generator.py spez llama-3.1-8b-instant")
        sys.exit(1)

    username = sys.argv[1]
    model_name = sys.argv[2] if len(sys.argv) > 2 else "llama-3.1-8b-instant"
    username = re.sub(r"^/?u/", "", username)

    print(f"Generating persona for Reddit user: {username} using Groq model: {model_name}")
    print("=" * 50)

    scraper = RedditScraper()
    analyzer = PersonaAnalyzer(model_name=model_name)

    print("1. Scraping user posts and comments...")
    posts, comments = scraper.get_user_content(username)

    if not posts and not comments:
        print(f"No usable content found for user {username}. Exiting.")
        sys.exit(0)

    print(f"   Found {len(posts)} posts and {len(comments)} comments with content.")

    print("2. Analyzing content with LLM...")
    persona = analyzer.analyze_content(posts, comments)
    persona.username = username

    print("3. Generating persona report...")
    formatted_output = PersonaFormatter.format_persona_to_text(persona)

    output_filename = f"{username}_persona_groq.txt"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(formatted_output)

    print(f"4. Persona saved to {output_filename}")


if __name__ == "__main__":
    main()
