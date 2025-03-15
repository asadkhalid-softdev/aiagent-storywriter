"""
Module for generating images based on prompts using OpenAI's DALL-E API.
"""
import time
import os
import sys
import requests
from io import BytesIO
from PIL import Image
from openai import OpenAI
from openai import APIError, RateLimitError, APIConnectionError
import logging

# Import configuration
sys.path.append(".")
from config.config import (
    OPENAI_API_KEY, IMAGE_MODEL, IMAGE_SIZE, 
    IMAGE_QUALITY, IMAGE_STYLE, OUTPUT_DIR
)


class ImageGenerator:
    def __init__(self, model=None):
        """
        Initialize the image generator with API client and parameters.
        
        Args:
            model (str, optional): Custom model to use. If None, uses default.
        """
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = model if model else IMAGE_MODEL
        self.size = IMAGE_SIZE
        self.quality = IMAGE_QUALITY
        self.style = IMAGE_STYLE
        self.max_retries = 3
        self.retry_delay = 5  # seconds
        
        logging.debug(f"Initialized ImageGenerator with model={self.model}")

    
    def generate_images(self, image_prompts, story_folder):
        """
        Generate images for the given prompts and save them to the story folder.
        
        Args:
            image_prompts (list): List of image prompts
            story_folder (str): Path to the folder where images should be saved
            
        Returns:
            list: Paths to the generated images
        """
        image_paths = []
        
        for i, prompt in enumerate(image_prompts):
            try:
                image_path = self._generate_single_image(prompt, story_folder, i+1)
                if image_path:
                    image_paths.append(image_path)
                    print(f"Generated image {i+1}/{len(image_prompts)}")
                else:
                    print(f"Failed to generate image {i+1}/{len(image_prompts)}")
            except Exception as e:
                print(f"Error generating image {i+1}: {str(e)}")
        
        return image_paths
    
    def _generate_single_image(self, prompt, story_folder, image_number):
        """
        Generate a single image and save it to disk.
        
        Args:
            prompt (str): The image prompt
            story_folder (str): Path to the story folder
            image_number (int): The sequence number of the image
            
        Returns:
            str: Path to the saved image, or None if generation failed
        """
        # Ensure the prompt is child-appropriate
        safe_prompt = self._ensure_safe_prompt(prompt)
        
        # Attempt to generate the image with retries
        for attempt in range(self.max_retries):
            try:
                print(f"Generating image {image_number} (attempt {attempt + 1})...")
                
                response = self.client.images.generate(
                    model=self.model,
                    prompt=safe_prompt,
                    size=self.size,
                    quality=self.quality,
                    style=self.style,
                    n=1
                )
                
                # Get the image URL
                image_url = response.data[0].url
                
                # Download and save the image
                image_filename = f"image_{image_number:02d}.png"
                image_path = os.path.join(story_folder, image_filename)
                
                # Download the image
                image_data = requests.get(image_url).content
                img = Image.open(BytesIO(image_data))
                
                # Save the image
                img.save(image_path)
                
                return image_path
                
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
                    return None
                time.sleep(self.retry_delay)
        
        return None
    
    def _ensure_safe_prompt(self, prompt):
        """
        Ensure the prompt is child-appropriate by adding safety instructions.
        
        Args:
            prompt (str): The original image prompt
            
        Returns:
            str: Enhanced prompt with safety instructions
        """
        # Add safety instructions to the prompt
        safety_instructions = (
            "Create a child-friendly, G-rated illustration suitable for young children. "
            "Use bright, cheerful colors and a non-threatening style. "
            "Ensure all content is age-appropriate for children ages 4-10. "
        )
        
        # Check if the prompt already has style instructions
        if "style:" in prompt.lower() or "style=" in prompt.lower():
            # Insert safety instructions before style instructions
            parts = prompt.split("Style:", 1) if "Style:" in prompt else prompt.split("style:", 1)
            enhanced_prompt = parts[0] + safety_instructions + "Style:" + parts[1]
        else:
            # Add safety instructions and style guidance
            enhanced_prompt = safety_instructions + prompt + " Style: children's book illustration, colorful, whimsical."
        
        return enhanced_prompt


if __name__ == "__main__":
    # Test the image generator
    generator = ImageGenerator()
    test_prompts = [
        "A friendly blue robot with big eyes playing in a park with children",
        "A little girl with brown hair showing a robot how to play on a swing"
    ]
    
    # Create a test folder
    test_folder = os.path.join(OUTPUT_DIR, "test_images")
    os.makedirs(test_folder, exist_ok=True)
    
    # Generate test images
    image_paths = generator.generate_images(test_prompts, test_folder)
    print(f"Generated {len(image_paths)} images in {test_folder}")
