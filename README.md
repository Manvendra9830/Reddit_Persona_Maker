# Reddit User Persona Generator

A Python script that scrapes Reddit user profiles, analyzes their posts and comments, and generates comprehensive user personas using AI analysis.

## Features

- **Reddit Scraping**: Extracts posts and comments from any public Reddit user
- **AI Analysis**: Uses OpenAI's GPT-4 to analyze content and generate insights
- **Comprehensive Personas**: Creates detailed user profiles including demographics, personality traits, motivations, behaviors, and goals
- **Citation System**: Provides specific citations for each piece of persona information
- **Clean Output**: Generates formatted text files with complete persona analysis

## Sample Output

The script generates personas similar to the example provided, including:
- Demographics (age, occupation, location, status)
- Personality traits on scales (introvert/extrovert, thinking/feeling, etc.)
- Motivations (convenience, wellness, speed, preferences, comfort, dietary needs)
- Behavioral patterns and habits
- Frustrations and pain points
- Goals and needs
- Key representative quotes
- User archetype and tier classification

## Requirements

- Python 3.7+
- Reddit API credentials
- OpenAI API key

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd reddit-persona-generator
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API credentials:**
   
   **Reddit API Setup:**
   - Go to https://www.reddit.com/prefs/apps
   - Click "Create App" or "Create Another App"
   - Choose "script" as the app type
   - Note down your client ID and client secret
   
   **OpenAI API Setup:**
   - Go to https://platform.openai.com/api-keys
   - Create a new API key
   - Copy the key (you won't be able to see it again)

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your actual credentials:
   ```
   REDDIT_CLIENT_ID=your_reddit_client_id
   REDDIT_CLIENT_SECRET=your_reddit_client_secret
   REDDIT_USER_AGENT=PersonaGenerator/1.0
   OPENAI_API_KEY=your_openai_api_key
   ```

## Usage

Run the script with a Reddit username:

```bash
python reddit_persona_generator.py <username>
```

**Examples:**
```bash
python reddit_persona_generator.py kojied
python reddit_persona_generator.py Hungry-Move-6603
```

The script will:
1. Scrape the user's posts and comments
2. Analyze the content using AI
3. Generate a comprehensive persona
4. Save the output to `<username>_persona.txt`

## Sample Commands for Project Users

```bash
# Generate persona for kojied
python reddit_persona_generator.py kojied

# Generate persona for Hungry-Move-6603
python reddit_persona_generator.py Hungry-Move-6603
```

## Output Format

The script generates a detailed text file with the following sections:

- **Demographics**: Age, occupation, location, relationship status, user tier, archetype
- **Personality Traits**: Scored on 1-10 scales for various personality dimensions
- **Motivations**: Rated importance of different factors (convenience, wellness, etc.)
- **Behavior & Habits**: Observed behavioral patterns
- **Frustrations**: Common pain points and complaints
- **Goals & Needs**: User objectives and requirements
- **Key Quote**: Representative statement from the user
- **Citations**: Specific post/comment references for each piece of information

## Project Structure

```
reddit-persona-generator/
├── reddit_persona_generator.py    # Main script
├── requirements.txt               # Python dependencies
├── .env.example                  # Environment template
├── README.md                     # This file
├── kojied_persona.txt            # Sample output (generated)
└── Hungry-Move-6603_persona.txt  # Sample output (generated)
```

## Technical Details

### Architecture

The script consists of four main components:

1. **RedditScraper**: Handles Reddit API interactions using PRAW
2. **PersonaAnalyzer**: Processes content using OpenAI's GPT-4
3. **PersonaFormatter**: Formats output into readable text
4. **Data Models**: Structured data classes for personas and citations

### AI Analysis Process

The script uses GPT-4 to analyze Reddit content and extract:
- Demographic information from contextual clues
- Personality traits based on communication patterns
- Motivations inferred from expressed preferences
- Behavioral patterns from posting habits
- Frustrations from complaint patterns
- Goals from expressed desires and needs

### Citation System

Every piece of persona information is backed by specific citations that include:
- Post/comment ID
- Content type (post or comment)
- Subreddit context
- Timestamp
- Direct URL to the source
- Relevant content excerpt

## Error Handling

The script includes comprehensive error handling for:
- Invalid usernames
- Private/suspended accounts
- API rate limits
- Network connectivity issues
- Missing API credentials

## Rate Limiting

The script respects Reddit's API rate limits and includes appropriate delays. For large-scale analysis, consider implementing additional rate limiting measures.

## Privacy and Ethics

This tool is designed for research and analysis purposes. Please use responsibly and respect user privacy:
- Only analyze public Reddit content
- Do not use for harassment or stalking
- Respect Reddit's terms of service
- Consider the ethical implications of persona analysis

## Troubleshooting

### Common Issues

1. **"Invalid credentials" error**: Check your Reddit API credentials in `.env`
2. **"User not found" error**: Verify the username is correct and the account exists
3. **"No content found" error**: User may have no posts/comments or a private profile
4. **OpenAI API errors**: Verify your API key and check your usage limits

### Debug Mode

To enable verbose output for debugging:
```bash
python reddit_persona_generator.py <username> --debug
```

## Dependencies

- **praw**: Reddit API wrapper for Python
- **openai**: OpenAI API client
- **python-dotenv**: Environment variable management

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the script.

## License

This project is provided as-is for educational and research purposes.

## API Costs

Note that this script uses OpenAI's GPT-4 API, which incurs costs based on usage. A typical persona generation uses approximately 2000-4000 tokens, costing around $0.06-$0.12 per analysis.