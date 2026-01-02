import json
import re
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

from .llm import LLM

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


class PersonaAnalyzer:
    """Analyzes Reddit content to generate user personas using an LLM."""

    def __init__(self, model_name: str = "llama3-8b-8192"):
        """Initialize the LLM client."""
        self.llm = LLM(model_name)

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

        # Truncate content if too long
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
            response = self.llm.get_response(prompt)

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

    def _clean_json_response(self, response: str) -> str:
        """Clean up the response to extract valid JSON."""
        # Remove markdown formatting
        response = re.sub(r"```json\s*", "", response)
        response = re.sub(r"```\s*$", "", response)

        # Remove comments in parentheses
        response = re.sub(r"\s*\([^)]*\)", "", response)

        # Fix invalid values (Not mentioned, Not specified, None) by quoting them
        response = re.sub(
            r'(:\s*)(Not mentioned|Not specified|None|N/A)(\s*[,\}])',
            r': "\2"\3', 
            response,
            flags=re.IGNORECASE
        )

        # Remove trailing commas
        response = re.sub(r",\s*([\}\]])", r"\1", response)

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
        self,
        analysis: Dict,
        content: List[Dict]
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
            if isinstance(cited_ids, list):
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
