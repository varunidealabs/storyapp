from src.azure_api import AzureOpenAI

class StoryGenerator:
    def __init__(self):
        self.azure_api = AzureOpenAI()
    
    def generate_story(self, genre: str, length: int, topic: str, character_name: str, keywords: str):
        """Generate a story ensuring it fully completes within a higher token limit.
        
        Args:
            genre (str): Story genre (Fantasy, Sci-Fi, etc.)
            length (int): Target word count
            topic (str): Theme/topic of the story, can include setting and era
            character_name (str): Main character name
            keywords (str): Comma-separated keywords
            
        Returns:
            tuple: (title, story_text)
        """
        keyword_list = [kw.strip() for kw in keywords.split(",") if kw.strip()]
        formatted_keywords = ", ".join(keyword_list)
        
        # Adjust `max_tokens` to ensure full completion
        max_token_limit = length * 1.5  # Allocate extra tokens to avoid truncation
        
        story_prompt = (
            f"Write a **complete {genre} short story** in **approximately {length} words**. "
            f"The story must have a **proper beginning, middle, and satisfying ending**. "
            f"Ensure the last sentence **completes the story logically** and does not get cut off. "
            f"\n\n**Story Details:**\n"
            f"- **Main Topic:** {topic}\n"
            f"- **Main Character:** {character_name}\n"
            f"- **Genre:** {genre} (Maintain appropriate tone, setting, and style)\n"
            f"- **Keywords:** {formatted_keywords} (Integrate these naturally)\n"
            f"\n\nCreate a story that is engaging, descriptive, and feels complete. "
            f"Use vivid descriptions and dialogue to bring the story to life. "
            f"Make the story emotionally resonant with a satisfying conclusion. "
            f"Carefully adhere to the {genre} genre conventions while being creative. "
            f"The final sentence must provide closure to the story. "
        )
        
        # Generate story with increased token limit
        story_response = self.azure_api.generate_response(story_prompt, max_tokens=int(max_token_limit))
        story_text = story_response.strip() if story_response else None
        
        # Generate title separately
        title_prompt = (
            f"Create a short, catchy title (5-8 words) for the following story. "
            f"The title should be evocative, intriguing, and reflect the {genre} genre. "
            f"Return ONLY the title (no quotes, no extra text).\n\nStory:\n{story_text[:500]}..."
        )
        
        title_response = self.azure_api.generate_response(title_prompt, max_tokens=15)
        story_title = title_response.strip() if title_response else "Untitled Story"
        
        return story_title, story_text
