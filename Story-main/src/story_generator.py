from src.azure_api import AzureOpenAI
class StoryGenerator:
    def __init__(self):
        self.azure_api = AzureOpenAI()

    def generate_story(self, genre: str, length: int, topic: str, character_name: str, keywords: str):
        """Generate a story ensuring it fully completes within a higher token limit."""
        keyword_list = [kw.strip() for kw in keywords.split(",") if kw.strip()]
        formatted_keywords = ", ".join(keyword_list)

        # Adjust `max_tokens` to ensure full completion
        max_token_limit = length * 1.5  # Allocate extra tokens to avoid truncation

        story_prompt = (
            f"Write a **self-contained {genre} short story** in **exactly {length} words**. "
            f"The story must have a **proper beginning, middle, and satisfying ending**. "
            f"Ensure the last sentence **completes the story logically** and does not get cut off. "
            f"\n\n**Story Details:**\n"
            f"- **Main Topic:** {topic}\n"
            f"- **Main Character:** {character_name}\n"
            f"- **Genre:** {genre} (Maintain an appropriate tone, setting, and style.)\n"
            f"- **Keywords:** {formatted_keywords} (Integrate these naturally.)\n"
            f"\n\nThe final sentence must be **a full, conclusive ending** (not cut off). "
            f"Ensure **precise word count adherence**—do not exceed or fall short of {length} words. "
            f"Use **frequent emojis** 🎭✨🔮 to enhance storytelling naturally. "
        )

        # ✅ Increase max_tokens to avoid truncation (1.5x buffer)
        story_response = self.azure_api.generate_response(story_prompt, max_tokens=int(max_token_limit))

        story_text = story_response.strip() if story_response else None

        # Generate title separately
        title_prompt = (
            f"Create a short, catchy title (5-10 words) for the following story. "
            f"Ensure the title reflects the theme and mood. "
            f"Return ONLY the title (no extra text).\n\nStory:\n{story_text}"
        )

        title_response = self.azure_api.generate_response(title_prompt, max_tokens=15)
        story_title = title_response.strip() if title_response else "Untitled Story"

        return story_title, story_text
