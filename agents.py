import os
from textwrap import dedent

from crewai import Agent
from crewai_tools import SerperDevTool
from custom_tools import ScrapeWebsiteTool, SunoTool
from callback_handler import CustomStreamlitCallbackHandler


class MelodyAgents:
    def __init__(self, url: str, genre: str, llm):
        self.llm = llm
        self.url = url
        self.genre = genre

        # Define some useful tools
        self.search_tool = SerperDevTool()
        self.scrape_website_tool = ScrapeWebsiteTool(limit=1000)
        self.suno_tool = SunoTool(url=self.url, genre=self.genre)

    @staticmethod
    def validate_prompt(prompt: str, char_limit: int = 1250) -> str:
        """Ensure the prompt does not exceed the character limit."""
        if len(prompt) > char_limit:
            print(f"Warning: Prompt exceeds {char_limit} characters. Trimming...")
            return prompt[:char_limit]
        return prompt

    def web_researcher_agent(self):
        return Agent(
            role="Web Researcher",
            goal="Conduct a web search on a topic, generating a detailed report on the matter. Ensure no prompt exceeds 250 words.",
            tools=[self.search_tool, self.scrape_website_tool],
            backstory=dedent("An expert in conducting web research on any topic."),
            verbose=True,
            allow_delegation=False,
            callbacks=[CustomStreamlitCallbackHandler(color="green")],
            llm=self.llm,
            max_rpm=4000,
            max_iter=6
        )

    def lyrics_creator_agent(self):
        return Agent(
            role="Lyrics Creator",
            goal=dedent("""Create amazing lyrics about a topic within 1250 characters,
                        adapting the writing style to the music genre."""),
            backstory="A creative lyricist who excels at creating high-quality lyrics within strict limits.",
            verbose=True,
            allow_delegation=False,
            callbacks=[CustomStreamlitCallbackHandler(color="green")],
            llm=self.llm,
            max_iter=3
        )

    def generate_song(self, topic: str):
        try:
            # Example lyrics generation logic
            generated_lyrics = self.llm.generate_text(
                f"Write lyrics about {topic} in the genre of {self.genre}."
            )

            # Validate the prompt to ensure it respects the character limit
            validated_lyrics = self.validate_prompt(generated_lyrics)

            # Use Suno tool to generate audio
            response = self.suno_tool.generate_audio(validated_lyrics)
            print("Song generated successfully!")
            return response

        except Exception as e:
            print(f"Error generating song: {e}")
            return None



