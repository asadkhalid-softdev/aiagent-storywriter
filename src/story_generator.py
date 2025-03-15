"""
Module for generating children's stories using OpenAI's GPT API.
"""
import time
import sys
from openai import OpenAI
from openai.types.chat import ChatCompletion
from openai import APIError, RateLimitError, APIConnectionError
import logging

# Import configuration
sys.path.append(".")
from config.config import OPENAI_API_KEY, STORY_MODEL, STORY_MAX_TOKENS, STORY_TEMPERATURE


class StoryGenerator:
    def __init__(self, model=None, temperature=None):
        """
        Initialize the story generator with API client and parameters.
        
        Args:
            model (str, optional): Custom model to use. If None, uses default.
            temperature (float, optional): Creativity level. If None, uses default.
        """
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = model if model else STORY_MODEL
        self.max_tokens = STORY_MAX_TOKENS
        self.temperature = temperature if temperature is not None else STORY_TEMPERATURE
        self.max_retries = 3
        self.retry_delay = 5  # seconds
        
        logging.debug(f"Initialized StoryGenerator with model={self.model}, temperature={self.temperature}")
    
    def generate_story(self, prompt):
        """
        Generate a children's story based on the provided prompt.
        
        Args:
            prompt (str): User's story idea or theme
            
        Returns:
            str: Generated story in markdown format
            
        Raises:
            Exception: If story generation fails after retries
        """
        # Create the system prompt for story generation
        system_prompt = """
        You are a creative children's story writer. Create an engaging, age-appropriate story for children 
        aged 4-10 years old based on the provided prompt. The story should:
        
        1. Be 500-1000 words long
        2. Have a clear beginning, middle, and end
        3. Include 1-3 main characters with distinct personalities
        4. Contain positive messages or lessons
        5. Use simple language appropriate for children
        6. Be engaging, imaginative, and fun
        7. Avoid any scary, violent, or inappropriate content
        8. Format the story in markdown with a title using # and paragraphs
        
        Return ONLY the story text in markdown format, with no additional explanations or notes.
        """
        
        # Enhanced user prompt with specific instructions
        user_prompt = f"""
        Create a children's story based on this idea: "{prompt}"
        
        Make the story whimsical, educational, and engaging for young readers.
        Include descriptive scenes that would work well as illustrations.
        """
        
        # Attempt to generate the story with retries
        for attempt in range(self.max_retries):
            try:
                print(f"Generating your children's story... (attempt {attempt + 1})")
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=self.max_tokens,
                    temperature=self.temperature
                )
                
                # Extract the story from the response
                story = response.choices[0].message.content.strip()
                
                # Ensure the story has a title
                if not story.startswith("# "):
                    # Extract a title from the first line or add a generic one
                    first_line = story.split("\n")[0]
                    title = first_line if len(first_line) < 50 else "My Children's Story"
                    story = f"# {title}\n\n{story}"
                
                return story
                
            except RateLimitError:
                print(f"Rate limit exceeded. Waiting {self.retry_delay} seconds before retrying...")
                time.sleep(self.retry_delay)
                self.retry_delay *= 2  # Exponential backoff
                
            except (APIError, APIConnectionError) as e:
                print(f"API error: {str(e)}. Retrying in {self.retry_delay} seconds...")
                time.sleep(self.retry_delay)
                
            except Exception as e:
                print(f"Unexpected error: {str(e)}")
                if attempt == self.max_retries - 1:
                    raise Exception(f"Failed to generate story after {self.max_retries} attempts: {str(e)}")
                time.sleep(self.retry_delay)
        
        raise Exception(f"Failed to generate story after {self.max_retries} attempts")


if __name__ == "__main__":
    # Test the story generator
    generator = StoryGenerator()
    test_prompt = "A friendly robot who learns about friendship"
    story = generator.generate_story(test_prompt)
    print(story)
