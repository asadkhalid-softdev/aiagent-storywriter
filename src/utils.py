"""
Utility functions for the AI Children's Story Generator.
"""
import re
import os
import sys
import logging
from pathlib import Path
from datetime import datetime


# ANSI color codes for terminal output
COLORS = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "reset": "\033[0m"
}


def print_colored(text, color="reset"):
    """
    Print text in the specified color.
    
    Args:
        text (str): The text to print
        color (str): The color to use
    """
    if color in COLORS and sys.stdout.isatty():  # Only use colors in a terminal
        print(f"{COLORS[color]}{text}{COLORS['reset']}")
    else:
        print(text)


def setup_logging(level="INFO", log_file=None):
    """
    Set up logging configuration.
    
    Args:
        level (str): Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file (str, optional): Path to log file. If None, logs to a default file.
    """
    # Convert string level to logging level
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(get_project_root(), "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    # Generate default log filename if not provided
    if not log_file:
        timestamp = datetime.now().strftime("%Y%m%d")
        log_file = os.path.join(logs_dir, f"story_generator_{timestamp}.log")
    
    # Configure logging
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler() if level.upper() == "DEBUG" else logging.NullHandler()
        ]
    )
    
    logging.info(f"Logging initialized at level {level}")


def extract_title_from_markdown(markdown_text):
    """
    Extract the title from markdown text.
    
    Args:
        markdown_text (str): The markdown text
        
    Returns:
        str: The extracted title
    """
    # Look for a markdown title
    title_match = re.search(r'^#\s+(.+)$', markdown_text, re.MULTILINE)
    if title_match:
        return title_match.group(1).strip()
    
    # If no markdown title, use the first line
    first_line = markdown_text.split('\n')[0].strip()
    if first_line:
        return first_line
    
    # Fallback
    return "Children's Story"


def clean_filename(text):
    """
    Clean text to make it suitable for a filename.
    
    Args:
        text (str): The text to clean
        
    Returns:
        str: Cleaned text
    """
    # Replace invalid filename characters
    text = re.sub(r'[\\/*?:"<>|]', '', text)
    
    # Replace spaces and other characters with underscores
    text = re.sub(r'[\s\-]+', '_', text)
    
    # Limit length
    text = text[:50]
    
    # Remove leading/trailing underscores
    text = text.strip('_')
    
    # Ensure the text is not empty
    if not text:
        text = "file"
    
    return text


def get_project_root():
    """
    Get the absolute path to the project root directory.
    
    Returns:
        str: Path to the project root
    """
    # Assuming this file is in src/utils.py
    return str(Path(__file__).parent.parent)


def ensure_dir_exists(directory):
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory (str): Path to the directory
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating directory {directory}: {str(e)}")
        return False


def count_words(text):
    """
    Count the number of words in a text.
    
    Args:
        text (str): The text to count words in
        
    Returns:
        int: Number of words
    """
    # Remove markdown formatting
    clean_text = re.sub(r'#+ ', '', text)  # Remove headers
    clean_text = re.sub(r'!\[.*?\]\(.*?\)', '', clean_text)  # Remove images
    clean_text = re.sub(r'\[.*?\]\(.*?\)', '', clean_text)  # Remove links
    
    # Split by whitespace and count
    words = clean_text.split()
    return len(words)


def format_time(seconds):
    """
    Format time in seconds to a human-readable string.
    
    Args:
        seconds (float): Time in seconds
        
    Returns:
        str: Formatted time string
    """
    if seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f} minutes"
    else:
        hours = seconds / 3600
        return f"{hours:.1f} hours"
