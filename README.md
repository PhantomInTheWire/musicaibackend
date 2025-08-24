# Music AI Backend

A FastAPI-based backend for AI-powered music generation and content processing.

## Features
- **Lyrics Generation**: Utilizes CrewAI agents with LangChain and Groq LLM for topic research and genre-specific lyrics creation.
- **Music Synthesis**: Integrates with Suno AI API for generating custom audio tracks from lyrics.
- **Web Scraping**: Employs custom tools for content scraping to enhance research tasks.
- **Audio Management**: Downloads and serves MP3 files via RESTful endpoints.

## Architecture
- **main.py**: FastAPI application handling endpoints like `/audio` for music generation workflow.
- **crew.py**: Manages CrewAI crew with agents (web_researcher, lyrics_creator) and tasks for research and lyrics.
- **tasks.py**: Defines CrewAI tasks for web research and lyrics creation with specific prompts.
- **custom_tools/**: Contains `suno_ai_tool.py` for AI music API interactions and `scraper_tool.py` for data scraping.

## Workflow
1. Receive topic and genre via `/audio` endpoint.
2. Execute CrewAI workflow to generate lyrics based on research.
3. Submit lyrics to Suno AI API for music generation.
4. Poll API for completion and download audio file.
5. Serve the generated MP3 as a response.

## Dependencies
- FastAPI, CrewAI, LangChain, Requests, python-dotenv.
- Requires API keys for Groq and Suno AI.

## Usage
Run `main.py` to start the server. Access `/audio?topic=example&genre=pop` to generate music.