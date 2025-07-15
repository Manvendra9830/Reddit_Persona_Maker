
# Reddit User Persona Generator

A Python script that scrapes Reddit user profiles, analyzes their posts and comments, and generates comprehensive user personas using local LLMs through **Ollama**.

## Features

- **Reddit Scraping**: Extracts posts and comments from any public Reddit user  
- **LLM Analysis with Ollama**: Uses models like `mistral`, `llama3.2`, and `llama3.1` via Ollama to analyze content  
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
- Ollama installed with any LLM models (mistral, llama3.1, llama3.2)

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

3. **Set up Reddit API credentials:**
   - Go to https://www.reddit.com/prefs/apps
   - Click "Create App" or "Create Another App"
   - Choose "script" as the app type
   - Note down your client ID and client secret

4. **Create `.env` file with your actual credentials:**
   ```
   REDDIT_CLIENT_ID=your_reddit_client_id
   REDDIT_CLIENT_SECRET=your_reddit_client_secret
   REDDIT_USER_AGENT=PersonaGenerator/1.0
   ```

## Ollama Setup

1. **Install Ollama**:  
   Download it from https://ollama.ai/download for your OS

2. **Download required models**:
   ```bash
   ollama pull mistral
   ollama pull llama3.2
   ollama pull llama3.1
   ```

3. **Start Ollama server** (if not already running):
   ```bash
   ollama serve
   ```

---

## Usage

Run the script with a Reddit username:

```bash
# Default (mistral)
python reddit_persona_generator.py <username>

# Specify a different model
python reddit_persona_generator.py <username> llama3.2
python reddit_persona_generator.py <username> llama3.1
```

**Examples:**
```bash
python reddit_persona_generator.py kojied
python reddit_persona_generator.py Hungry-Move-6603 llama3.2
```

The script will:
1. Scrape the user's posts and comments  
2. Analyze the content using the chosen LLM model via Ollama  
3. Generate a comprehensive persona  
4. Save the output to `<username>_persona_<model>.txt`

## Output Format

The script generates a detailed text file with the following sections:

- **Demographics**: Age, occupation, location, relationship status, user tier, archetype  
- **Personality Traits**: Scored on 1–10 scales for various personality dimensions  
- **Motivations**: Rated importance of factors like convenience, wellness, etc.  
- **Behavior & Habits**: Observed behavioral patterns  
- **Frustrations**: Common pain points  
- **Goals & Needs**: User objectives and aspirations  
- **Key Quote**: Representative user statement  
- **Citations**: Reddit post/comment references for each attribute  

## Project Structure

```
reddit-persona-generator/
├── reddit_persona_generator.py     # Main script
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
├── README.md                       # This file
├── kojied_persona_mistral.txt      # Sample output (generated)
└── Hungry-Move-6603_persona_llama3.2.txt  # Sample output (generated)
```

## Technical Details

### Architecture

1. **RedditScraper** – Uses PRAW to fetch user posts/comments  
2. **PersonaAnalyzer** – Sends content to the Ollama API for model analysis  
3. **PersonaFormatter** – Converts analysis into a readable text persona  
4. **Data Models** – Structured classes for personas and citations  

### AI Analysis Process

The selected Ollama LLM model analyzes Reddit content to extract:
- Demographics from context clues  
- Personality traits based on communication style  
- Motivations from stated preferences  
- Behavioral patterns from posting habits  
- Frustrations from complaints or rants  
- Goals from expressed desires or needs  

### Citation System

Each piece of information is supported by:
- Post or comment ID  
- Type (post/comment)  
- Subreddit context  
- Date  
- URL to the original source  
- A snippet of the referenced content  

---

## Error Handling

The script handles:
- Invalid usernames  
- Private or suspended accounts  
- API rate limits  
- Network errors  
- Missing environment variables  

---

## Privacy and Ethics

Use this tool responsibly. Respect user privacy:

- Only analyze **public Reddit content**  
- Don’t use for profiling, stalking, or unethical targeting  
- Follow [Reddit API Terms](https://www.reddit.com/wiki/api-terms)  

---

## Troubleshooting

**Common Issues:**

1. **Invalid credentials** – Check `.env`  
2. **User not found** – Confirm Reddit username  
3. **No content** – Might be a private/restricted account  
4. **Ollama not responding** – Ensure `ollama serve` is running  

**Debug Mode:**
```bash
python reddit_persona_generator.py <username> --debug
```

---

## Dependencies

- `praw` – Reddit API wrapper  
- `ollama` – Local LLM interface  
- `requests`, `python-dotenv` – Utility libraries

---

## Contributing

Feel free to open issues, suggest improvements, or submit pull requests.

---

## License

This project is for educational and research purposes only.
