import os
from typing import Dict, List, Tuple
import praw
from dotenv import load_dotenv

load_dotenv()

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
