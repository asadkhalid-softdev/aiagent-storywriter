"""
Module for extracting key scenes from a story and creating image prompts.
"""
import re
import sys
from openai import OpenAI

# Import configuration
sys.path.append(".")
from config.config import OPENAI_API_KEY, STORY_MODEL, IMAGES_PER_STORY


class ImagePromptCreator:
    def __init__(self):
        """Initialize the image prompt creator."""
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = STORY_MODEL
        self.num_images = IMAGES_PER_STORY
    
    def extract_scenes(self, story_text):
        """
        Extract key scenes from the story for image generation.
        
        Args:
            story_text (str): The generated story text
            
        Returns:
            list: List of image prompts for key scenes
        """
        # Extract title for context
        title = self._extract_title(story_text)
        
        # Create a system prompt for scene extraction
        system_prompt = f"""
        You are an expert at identifying key visual scenes from children's stories.
        Your task is to identify exactly {self.num_images} key scenes from the provided story 
        that would make good illustrations for a children's book.
        
        For each scene:
        1. Choose visually interesting moments that advance the story
        2. Focus on the main characters and important story elements
        3. Distribute scenes evenly throughout the story (beginning, middle, end)
        4. Create detailed, specific image prompts that a text-to-image AI can use
        5. Make each prompt child-appropriate and visually appealing
        6. Include specific details about characters, setting, actions, and mood
        7. Format each prompt to be 1-3 sentences long
        
        Return ONLY a JSON array of {self.num_images} image prompts, with no additional text.
        Each prompt should be a string in the array.
        """
        
        # User prompt with the story
        user_prompt = f"""
        Story Title: {title}
        
        Story Text:
        {story_text}
        
        Identify exactly {self.num_images} key scenes from this story that would make good illustrations.
        Return them as a JSON array of strings, with each string being a detailed image prompt.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            # Extract the JSON response
            content = response.choices[0].message.content.strip()
            
            # Clean up the response to extract just the array
            import json
            try:
                # Parse the JSON response
                parsed_response = json.loads(content)
                
                # Extract the array of prompts (handle different possible formats)
                if isinstance(parsed_response, list):
                    image_prompts = parsed_response
                elif "prompts" in parsed_response:
                    image_prompts = parsed_response["prompts"]
                elif "scenes" in parsed_response:
                    image_prompts = parsed_response["scenes"]
                else:
                    # Try to find any array in the response
                    for key, value in parsed_response.items():
                        if isinstance(value, list):
                            image_prompts = value
                            break
                    else:
                        # If no array found, use the first N items if it's a dict
                        image_prompts = list(parsed_response.values())[:self.num_images]
                
                # Ensure we have the right number of prompts
                image_prompts = image_prompts[:self.num_images]
                
                # Add child-friendly instruction to each prompt
                enhanced_prompts = []
                for prompt in image_prompts:
                    # Ensure prompt is a string
                    if not isinstance(prompt, str):
                        prompt = str(prompt)
                    
                    # Add style instructions for child-friendly illustrations
                    enhanced_prompt = f"{prompt} Style: colorful children's book illustration, child-friendly, whimsical, detailed, vibrant colors, digital art."
                    enhanced_prompts.append(enhanced_prompt)
                
                return enhanced_prompts
                
            except json.JSONDecodeError:
                # Fallback: try to extract prompts using regex if JSON parsing fails
                print("Warning: Could not parse JSON response. Attempting to extract prompts manually.")
                pattern = r'"([^"]+)"'
                matches = re.findall(pattern, content)
                
                if matches and len(matches) >= self.num_images:
                    return [f"{match} Style: colorful children's book illustration, child-friendly, whimsical." 
                            for match in matches[:self.num_images]]
                else:
                    # Last resort: split by numbered list if available
                    lines = content.split("\n")
                    prompts = []
                    for line in lines:
                        if re.match(r'^\d+[\.\)]\s', line):  # Matches numbered lists like "1. " or "1) "
                            prompt_text = re.sub(r'^\d+[\.\)]\s', '', line).strip()
                            if prompt_text:
                                prompts.append(f"{prompt_text} Style: colorful children's book illustration, child-friendly.")
                    
                    if prompts and len(prompts) >= self.num_images:
                        return prompts[:self.num_images]
            
            # If all parsing attempts fail, create generic prompts
            return self._create_generic_prompts(title, story_text)
            
        except Exception as e:
            print(f"Error extracting scenes: {str(e)}")
            return self._create_generic_prompts(title, story_text)
    
    def _extract_title(self, story_text):
        """Extract the title from the story text."""
        # Look for a markdown title
        title_match = re.search(r'^#\s+(.+)$', story_text, re.MULTILINE)
        if title_match:
            return title_match.group(1).strip()
        
        # If no markdown title, use the first line
        first_line = story_text.split('\n')[0].strip()
        if first_line:
            return first_line
        
        # Fallback
        return "Children's Story"
    
    def _create_generic_prompts(self, title, story_text):
        """Create generic image prompts based on the story title and text."""
        # Extract character names (simple approach)
        words = re.findall(r'\b[A-Z][a-z]+\b', story_text)
        potential_characters = [word for word in words if len(word) > 3 and word not in ["The", "This", "That", "There", "They", "Then"]]
        
        # Get most common potential character names
        from collections import Counter
        character_counts = Counter(potential_characters)
        main_characters = [char for char, count in character_counts.most_common(3) if count > 1]
        
        # Create generic prompts
        prompts = []
        
        # Title/introduction scene
        prompts.append(f"The main scene from the children's story '{title}'. Colorful illustration, child-friendly style, whimsical setting.")
        
        # Character-based scenes
        for character in main_characters[:2]:
            prompts.append(f"{character} from the story '{title}', engaging in an adventure. Colorful children's book illustration style, child-friendly, detailed.")
        
        # Conclusion scene
        prompts.append(f"The happy ending scene from the children's story '{title}'. Colorful, warm, and joyful illustration in a child-friendly style.")
        
        # Fill remaining slots if needed
        while len(prompts) < self.num_images:
            prompts.append(f"An exciting scene from the children's story '{title}'. Vibrant colors, child-friendly illustration style, whimsical and engaging.")
        
        return prompts[:self.num_images]


if __name__ == "__main__":
    # Test the image prompt creator
    creator = ImagePromptCreator()
    test_story = """
    # The Friendly Robot
    
    Once upon a time, there was a robot named Beep who lived alone in a small workshop. Beep could do many things, but he didn't have any friends.
    
    One day, Beep decided to go to the nearby park. There, he saw children playing together and having fun. Beep wanted to join them, but he was afraid they wouldn't like him.
    
    A little girl named Lily noticed Beep watching from a distance. She walked over and said, "Hello! Would you like to play with us?"
    
    Beep was surprised but happy. "I'd love to," he replied with a mechanical voice that made Lily smile.
    
    Soon, Beep was playing games with all the children. He learned that friendship means sharing, listening, and being kind to others.
    
    From that day on, Beep visited the park every afternoon. He had found something more valuable than any program or tool – he had found friendship.
    """
    
    prompts = creator.extract_scenes(test_story)
    for i, prompt in enumerate(prompts, 1):
        print(f"Image {i}: {prompt}")
