# Music AI Backend

This project delivers an AI-driven music generation system using **FastAPI** for the backend. It leverages advanced AI tools to create custom songs from user-defined topics and genres.

The core functionality revolves around generating lyrics through intelligent agents powered by *CrewAI* and *LangChain*. These agents research topics and craft genre-specific lyrics, ensuring high-quality content.

Music synthesis is handled via the *Suno AI API*, which transforms lyrics into audio tracks. The system also includes web scraping capabilities to gather relevant data for enhanced research.

Key components include `main.py` for API endpoints, `crew.py` for agent management, and custom tools in the `custom_tools/` directory. Dependencies such as `FastAPI`, `CrewAI`, and `Requests` are essential for operation.

To use, execute `python main.py` and query the `/audio` endpoint with parameters like `topic` and `genre`. The process involves research, lyrics creation, API submission, and audio delivery.

*Note: API keys for Groq and Suno AI are required for full functionality.*

- Ghost