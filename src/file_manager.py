"""
Module for handling file operations, including creating directories and saving content.
"""
import os
import re
import datetime
import sys
import logging
from pathlib import Path

# Import configuration
sys.path.append(".")
from config.config import OUTPUT_DIR


class FileManager:
    def __init__(self, custom_output_dir=None):
        """
        Initialize the file manager.
        
        Args:
            custom_output_dir (str, optional): Custom output directory. If None, uses default.
        """
        self.output_dir = custom_output_dir if custom_output_dir else OUTPUT_DIR
        self.ensure_output_dir_exists()
    
    def ensure_output_dir_exists(self):
        """Ensure the output directory exists."""
        os.makedirs(self.output_dir, exist_ok=True)
        logging.debug(f"Ensured output directory exists: {self.output_dir}")
    
    def create_story_folder(self, story_title):
        """
        Create a folder for the story based on its title and current timestamp.
        
        Args:
            story_title (str): The title of the story
            
        Returns:
            str: Path to the created folder
        """
        # Clean the title to make it suitable for a folder name
        clean_title = self._clean_title(story_title)
        
        # Generate timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create folder name with title and timestamp
        folder_name = f"{clean_title}_{timestamp}"
        
        # Create the full path
        folder_path = os.path.join(self.output_dir, folder_name)
        
        # Create the folder
        os.makedirs(folder_path, exist_ok=True)
        
        logging.info(f"Created story folder: {folder_path}")
        return folder_path
    
    def save_story_markdown(self, story_text, folder_path):
        """
        Save the story text as a markdown file.
        
        Args:
            story_text (str): The story content in markdown format
            folder_path (str): Path to the story folder
            
        Returns:
            str: Path to the saved markdown file
        """
        # Extract title from the markdown
        title = self._extract_title(story_text)
        clean_title = self._clean_title(title)
        
        # Create filename
        filename = f"{clean_title}.md"
        file_path = os.path.join(folder_path, filename)
        
        # Save the story
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(story_text)
        
        logging.info(f"Saved story markdown to: {file_path}")
        return file_path
    
    def update_markdown_with_images(self, markdown_path, image_paths):
        """
        Update the markdown file to include the generated images.
        
        Args:
            markdown_path (str): Path to the markdown file
            image_paths (list): List of paths to the generated images
            
        Returns:
            str: Path to the updated markdown file
        """
        # Read the original markdown
        with open(markdown_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find appropriate places to insert images
        paragraphs = re.split(r'\n\n+', content)
        
        # Calculate how many paragraphs per image (approximately)
        if len(paragraphs) <= 1 or not image_paths:
            # Not enough paragraphs or no images
            logging.warning("Not enough paragraphs or no images to insert")
            return markdown_path
        
        # Determine insertion points (after intro, before conclusion, and in between)
        num_images = len(image_paths)
        step = max(1, (len(paragraphs) - 2) // (num_images))
        
        # Start after the title (index 1) and leave the last paragraph
        insertion_points = list(range(1, len(paragraphs) - 1, step))[:num_images]
        
        # Insert images at the determined points
        for i, point in enumerate(insertion_points):
            if i < len(image_paths):
                # Get relative path for the image
                image_filename = os.path.basename(image_paths[i])
                image_markdown = f"\n\n![Image {i+1}]({image_filename})\n\n"
                paragraphs.insert(point + i, image_markdown)
        
        # Join the paragraphs back together
        updated_content = '\n\n'.join(paragraphs)
        
        # Save the updated markdown
        with open(markdown_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        logging.info(f"Updated markdown with {len(image_paths)} images")
        return markdown_path
    
    def _clean_title(self, title):
        """
        Clean a title to make it suitable for a filename.
        
        Args:
            title (str): The title to clean
            
        Returns:
            str: Cleaned title
        """
        # Remove markdown formatting if present
        title = re.sub(r'^#\s+', '', title)
        
        # Replace invalid filename characters
        title = re.sub(r'[\\/*?:"<>|]', '', title)
        
        # Replace spaces and other characters with underscores
        title = re.sub(r'[\s\-]+', '_', title)
        
        # Limit length
        title = title[:50]
        
        # Remove leading/trailing underscores
        title = title.strip('_')
        
        # Ensure the title is not empty
        if not title:
            title = "story"
        
        logging.debug(f"Cleaned title: '{title}'")
        return title
    
    def _extract_title(self, markdown_text):
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

