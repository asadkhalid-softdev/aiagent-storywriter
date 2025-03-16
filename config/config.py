"""
Configuration settings for the AI Children's Story Generator.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Version information
VERSION = "1.0.0"

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Story Generation Settings
STORY_MODEL = "gpt-4o"  # Model to use for story generation
STORY_MAX_TOKENS = 2000  # Maximum tokens for story generation
STORY_TEMPERATURE = 0.7  # Creativity level (0.0-1.0)

# Image Generation Settings
IMAGE_MODEL = "dall-e-3"  # Model to use for image generation
IMAGE_SIZE = "1024x1024"  # Size of generated images
IMAGE_QUALITY = "standard"  # Quality of generated images
IMAGE_STYLE = "natural"  # Style of generated images

# Output Settings
OUTPUT_DIR = "output"  # Directory to save generated stories and images
IMAGES_PER_STORY = 4  # Number of images to generate per story

# Content Safety
CONTENT_FILTER = True  # Enable content filtering for child-appropriate content

# Logging Configuration
LOG_LEVEL = "INFO"  # Default logging level
LOG_DIR = "logs"  # Directory for log files
