"""
Main entry point for the AI Children's Story Generator.
This script integrates all modules to create a complete story generation system.
"""
import sys
import os
import logging
import time
from src.input_handler import InputHandler
from src.story_generator import StoryGenerator
from src.image_prompt_creator import ImagePromptCreator
from src.image_generator import ImageGenerator
from src.file_manager import FileManager
from src.utils import setup_logging, print_colored
from src.cli import parse_arguments, print_welcome_message, list_generated_stories, show_version_info
from src.content_filter import ContentFilter
from src.performance_monitor import PerformanceMonitor
from src.prompt_optimizer import PromptOptimizer
from config.config import OPENAI_API_KEY, OUTPUT_DIR

def check_api_key():
    """Check if the API key is set."""
    if not OPENAI_API_KEY:
        print_colored("Error: OpenAI API key is not set.", "red")
        print_colored("Please set your API key in the .env file or config/config.py", "yellow")
        sys.exit(1)


def generate_story(story_prompt=None, num_images=None, output_dir=None, verbose=False, model=None, 
                  image_model=None, temperature=None, optimize_prompts=False, filter_content=True):
    """
    Generate a story based on the provided prompt.
    
    Args:
        story_prompt (str, optional): The story prompt. If None, will prompt the user.
        num_images (int, optional): Number of images to generate. If None, uses default.
        output_dir (str, optional): Custom output directory. If None, uses default.
        verbose (bool): Whether to print verbose output.
        model (str, optional): Custom GPT model to use.
        image_model (str, optional): Custom image model to use.
        temperature (float, optional): Creativity level for story generation.
        optimize_prompts (bool): Whether to optimize prompts for better quality.
        filter_content (bool): Whether to filter content for child-appropriateness.
        
    Returns:
        tuple: (success, story_folder_path)
    """
    # Initialize performance monitoring
    monitor = PerformanceMonitor()
    monitor.start_monitoring()
    
    # Initialize modules
    input_handler = InputHandler()
    story_generator = StoryGenerator(model=model, temperature=temperature)
    image_prompt_creator = ImagePromptCreator()
    image_generator = ImageGenerator(model=image_model)
    file_manager = FileManager(custom_output_dir=output_dir)
    content_filter = ContentFilter() if filter_content else None
    prompt_optimizer = PromptOptimizer() if optimize_prompts else None
    
    try:
        # Get user input if not provided
        monitor.start_operation("Input Handling")
        if not story_prompt:
            story_prompt = input_handler.get_story_prompt()
        else:
            # Validate the provided prompt
            validation = input_handler.validate_input(story_prompt)
            if not validation["valid"]:
                logging.error(f"Invalid prompt: {validation['message']}")
                print_colored(f"Error: {validation['message']}", "red")
                monitor.end_operation("Input Handling")
                return False, None
        monitor.end_operation("Input Handling")
        
        # Optimize the prompt if requested
        if optimize_prompts and prompt_optimizer:
            monitor.start_operation("Prompt Optimization")
            print_colored("Optimizing your prompt for better story quality...", "blue")
            # For initial prompt, we'll use a simple enhancement
            enhanced_prompt = story_prompt + " Make it engaging, educational, and appropriate for children ages 4-10 with clear scenes that would work well as illustrations."
            story_prompt = enhanced_prompt
            monitor.end_operation("Prompt Optimization")
        
        logging.info(f"Generating story with prompt: {story_prompt}")
        print_colored("\nGenerating your story. This may take a moment...", "blue")
        
        # Generate the story
        monitor.start_operation("Story Generation")
        start_time = time.time()
        story_text = story_generator.generate_story(story_prompt)
        generation_time = time.time() - start_time
        logging.info(f"Story generated in {generation_time:.2f} seconds")
        monitor.end_operation("Story Generation")
        
        if verbose:
            print_colored(f"Story generation completed in {generation_time:.2f} seconds", "green")
        
        # Filter content if requested
        if filter_content and content_filter:
            monitor.start_operation("Content Filtering")
            print_colored("Checking content for child-appropriateness...", "blue")
            check_result = content_filter.check_story_content(story_text)
            
            if not check_result["is_appropriate"]:
                print_colored("Filtering inappropriate content...", "yellow")
                if verbose:
                    for issue in check_result["pattern_issues"]:
                        print_colored(f"  - Found '{issue['word']}' in context: \"{issue['context']}\"", "yellow")
                
                story_text = content_filter.filter_story_content(story_text)
                print_colored("Content filtering complete", "green")
            else:
                print_colored("Content check passed", "green")
            
            monitor.end_operation("Content Filtering")
        
        # Extract title for folder creation
        title_match = story_text.split('\n')[0]
        if title_match.startswith('# '):
            title = title_match[2:]
        else:
            title = "Children's Story"
        
        # Create a folder for the story
        monitor.start_operation("File Management")
        story_folder = file_manager.create_story_folder(title)
        logging.info(f"Created story folder: {story_folder}")
        
        # Save the story as markdown
        markdown_path = file_manager.save_story_markdown(story_text, story_folder)
        logging.info(f"Saved story to: {markdown_path}")
        monitor.end_operation("File Management")
        
        print_colored("\nCreating image prompts from your story...", "blue")
        
        # Extract scenes for image generation
        monitor.start_operation("Image Prompt Creation")
        start_time = time.time()
        image_prompts = image_prompt_creator.extract_scenes(story_text)
        extraction_time = time.time() - start_time
        logging.info(f"Extracted {len(image_prompts)} image prompts in {extraction_time:.2f} seconds")
        monitor.end_operation("Image Prompt Creation")
        
        # Optimize image prompts if requested
        if optimize_prompts and prompt_optimizer:
            monitor.start_operation("Image Prompt Optimization")
            print_colored("Optimizing image prompts for better quality...", "blue")
            image_prompts = prompt_optimizer.optimize_image_prompts(story_text, image_prompts)
            monitor.end_operation("Image Prompt Optimization")
        
        # Filter image prompts if requested
        if filter_content and content_filter:
            monitor.start_operation("Image Prompt Filtering")
            filtered_prompts = []
            for prompt in image_prompts:
                filtered_prompts.append(content_filter.filter_image_prompt(prompt))
            image_prompts = filtered_prompts
            monitor.end_operation("Image Prompt Filtering")
        
        if verbose:
            print_colored(f"Created {len(image_prompts)} image prompts in {extraction_time:.2f} seconds", "green")
            for i, prompt in enumerate(image_prompts, 1):
                print_colored(f"Image {i} prompt: {prompt[:100]}...", "cyan")
        
        print_colored(f"\nGenerating {len(image_prompts)} images for your story...", "blue")
        
        # Generate images
        monitor.start_operation("Image Generation")
        start_time = time.time()
        image_paths = image_generator.generate_images(image_prompts, story_folder)
        image_time = time.time() - start_time
        logging.info(f"Generated {len(image_paths)} images in {image_time:.2f} seconds")
        monitor.end_operation("Image Generation")
        
        if verbose:
            print_colored(f"Generated {len(image_paths)} images in {image_time:.2f} seconds", "green")
        
        # Update the markdown with images
        monitor.start_operation("Markdown Update")
        file_manager.update_markdown_with_images(markdown_path, image_paths)
        logging.info(f"Updated markdown with {len(image_paths)} images")
        monitor.end_operation("Markdown Update")
        
        # Save performance data
        monitor.stop_monitoring()
        performance_dir = os.path.join(story_folder, "performance")
        monitor.save_performance_data(performance_dir)
        
        # If prompt optimization was used, save analysis
        if optimize_prompts and prompt_optimizer:
            analysis = prompt_optimizer.analyze_story_quality(story_text, story_prompt)
            prompt_optimizer.save_optimization_results(analysis, story_prompt, story_text, performance_dir)
            
            if verbose:
                print_colored("\nStory Quality Analysis:", "cyan")
                print_colored(f"Overall Rating: {analysis.get('overall_rating', 'N/A')}/10", "green")
                print_colored("Strengths:", "green")
                for strength in analysis.get('strengths', [])[:3]:  # Show top 3 strengths
                    print_colored(f"  - {strength}", "green")
        
        print_colored("\n===== Story Generation Complete =====", "green")
        print_colored(f"Your story has been saved to: {os.path.abspath(markdown_path)}", "green")
        print_colored(f"Generated {len(image_paths)} images in: {os.path.abspath(story_folder)}", "green")
        
        return True, story_folder
        
    except Exception as e:
        logging.error(f"Error in story generation: {str(e)}", exc_info=True)
        print_colored(f"\nError: {str(e)}", "red")
        print_colored("Story generation failed. Please try again.", "yellow")
        
        # Stop monitoring and save what we have
        monitor.stop_monitoring()
        monitor.save_performance_data()
        
        return False, None

def main():
    """Main function to run the story generator with command-line arguments."""
    # Parse command-line arguments
    args = parse_arguments()
    
    # Setup logging
    setup_logging(level=args.log)
    
    # Handle special actions
    if args.version:
        show_version_info()
        return 0
    
    if args.list_stories:
        list_generated_stories(args.output or OUTPUT_DIR)
        return 0
    
    # Handle test mode
    if args.test:
        from src.test_app import run_tests
        run_tests(save_results=True, verbose=args.verbose)
        return 0
    
    # Print welcome message
    print_welcome_message()
    
    # Check API key
    check_api_key()
    
    # Add new arguments for Phase 5
    optimize = getattr(args, 'optimize', False)
    filter_content = not getattr(args, 'no_filter', False)
    
    # Generate the story
    success, _ = generate_story(
        story_prompt=args.prompt,
        num_images=args.images,
        output_dir=args.output,
        verbose=args.verbose,
        model=args.model,
        image_model=args.image_model,
        temperature=args.temperature,
        optimize_prompts=optimize,
        filter_content=filter_content
    )
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
