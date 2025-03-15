"""
Command-line interface for the AI Children's Story Generator.
"""
import sys
import os
import argparse
import logging
from src.utils import print_colored, setup_logging
from config.config import VERSION

def parse_arguments():
    """
    Parse command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description=f"AI Children's Story Generator v{VERSION}",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Basic arguments
    parser.add_argument('-p', '--prompt', type=str, 
                        help='Story prompt (if not provided, will prompt interactively)')
    parser.add_argument('-i', '--images', type=int, 
                        help='Number of images to generate')
    parser.add_argument('-o', '--output', type=str, 
                        help='Custom output directory')
    
    # Verbosity and logging
    parser.add_argument('-v', '--verbose', action='store_true', 
                        help='Enable verbose output')
    parser.add_argument('--log', type=str, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], 
                        default='INFO', help='Set logging level')
    
    # Advanced options
    advanced_group = parser.add_argument_group('Advanced Options')
    advanced_group.add_argument('--model', type=str, 
                               help='Specify GPT model for story generation')
    advanced_group.add_argument('--image-model', type=str, 
                               help='Specify model for image generation')
    advanced_group.add_argument('--temperature', type=float, 
                               help='Creativity level (0.0-1.0) for story generation')
    
    # Phase 5 additions
    advanced_group.add_argument('--optimize', action='store_true',
                               help='Optimize prompts for better quality')
    advanced_group.add_argument('--no-filter', action='store_true',
                               help='Disable content filtering')
    advanced_group.add_argument('--test', action='store_true',
                               help='Run test suite with sample prompts')
    
    # Actions
    action_group = parser.add_argument_group('Actions')
    action_group.add_argument('--list-stories', action='store_true', 
                             help='List all generated stories')
    action_group.add_argument('--version', action='store_true', 
                             help='Show version information and exit')
    
    return parser.parse_args()

def print_welcome_message():
    """Print welcome message with ASCII art."""
    welcome_text = f"""
    ╔═══════════════════════════════════════════════╗
    ║                                               ║
    ║       AI Children's Story Generator           ║
    ║                 v{VERSION:<8}                     ║
    ║                                               ║
    ╚═══════════════════════════════════════════════╝
    """
    print_colored(welcome_text, "cyan")

def list_generated_stories(output_dir):
    """
    List all generated stories in the output directory.
    
    Args:
        output_dir (str): Path to the output directory
    """
    if not os.path.exists(output_dir):
        print_colored(f"Output directory not found: {output_dir}", "yellow")
        return
    
    # Get all subdirectories in the output directory
    story_folders = [d for d in os.listdir(output_dir) 
                    if os.path.isdir(os.path.join(output_dir, d))]
    
    if not story_folders:
        print_colored("No stories found.", "yellow")
        return
    
    # Sort by creation time (newest first)
    story_folders.sort(key=lambda d: os.path.getctime(os.path.join(output_dir, d)), reverse=True)
    
    print_colored(f"\nFound {len(story_folders)} stories:", "green")
    print_colored("=" * 60, "blue")
    
    for i, folder in enumerate(story_folders, 1):
        folder_path = os.path.join(output_dir, folder)
        creation_time = os.path.getctime(folder_path)
        
        # Find markdown files
        md_files = [f for f in os.listdir(folder_path) if f.endswith('.md')]
        
        # Find image files
        image_files = [f for f in os.listdir(folder_path) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        # Print story information
        from datetime import datetime
        time_str = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
        
        print_colored(f"{i}. {folder}", "cyan")
        print(f"   Created: {time_str}")
        print(f"   Story file: {md_files[0] if md_files else 'None'}")
        print(f"   Images: {len(image_files)}")
        print_colored("   " + "-" * 56, "blue")
    
    print_colored("=" * 60, "blue")

def show_version_info():
    """Show detailed version information."""
    import platform
    import openai
    
    print_colored(f"\nAI Children's Story Generator v{VERSION}", "cyan")
    print(f"Python version: {platform.python_version()}")
    print(f"Operating system: {platform.system()} {platform.release()}")
    
    try:
        print(f"OpenAI library version: {openai.__version__}")
    except (ImportError, AttributeError):
        print("OpenAI library: Unknown version")
    
    print("\nCreated by: Your Name")
    print("License: MIT")
    print("Repository: https://github.com/yourusername/story-generator")
