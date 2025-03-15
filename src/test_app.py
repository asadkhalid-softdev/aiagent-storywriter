"""
Module for testing the AI Children's Story Generator with various inputs.
"""
import os
import sys
import time
import logging
from pathlib import Path

# Add project root to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from src.input_handler import InputHandler
from src.story_generator import StoryGenerator
from src.image_prompt_creator import ImagePromptCreator
from src.image_generator import ImageGenerator
from src.file_manager import FileManager
from src.utils import setup_logging, print_colored
from config.config import OUTPUT_DIR


def run_tests(test_inputs=None, save_results=True, verbose=True):
    """
    Run tests on the story generator with various inputs.
    
    Args:
        test_inputs (list, optional): List of test prompts. If None, uses default test cases.
        save_results (bool): Whether to save the generated stories and images.
        verbose (bool): Whether to print detailed output.
        
    Returns:
        dict: Test results summary
    """
    # Setup logging
    setup_logging(level="INFO")
    
    # Define default test inputs if none provided
    if test_inputs is None:
        test_inputs = [
            "A friendly dragon who helps children learn about recycling",
            "A magical forest where animals talk and help a lost child find their way home",
            "A robot who learns the value of friendship while exploring a new planet",
            "A young girl who discovers she can talk to the stars and learns about constellations",
            "A group of kids who work together to save their town from a flood using teamwork and creativity"
        ]
    
    # Initialize components
    input_handler = InputHandler()
    story_generator = StoryGenerator()
    image_prompt_creator = ImagePromptCreator()
    image_generator = ImageGenerator()
    
    # Create test output directory
    test_output_dir = os.path.join(OUTPUT_DIR, "test_results")
    if save_results:
        os.makedirs(test_output_dir, exist_ok=True)
    
    file_manager = FileManager(custom_output_dir=test_output_dir if save_results else None)
    
    # Track test results
    results = {
        "total_tests": len(test_inputs),
        "successful_tests": 0,
        "failed_tests": 0,
        "story_generation_times": [],
        "image_generation_times": [],
        "total_images_generated": 0,
        "average_story_length": 0,
        "test_details": []
    }
    
    # Run tests
    print_colored("\n===== Running Story Generator Tests =====\n", "cyan")
    
    total_story_length = 0
    
    for i, test_input in enumerate(test_inputs, 1):
        print_colored(f"Test {i}/{len(test_inputs)}: {test_input}", "blue")
        
        test_result = {
            "prompt": test_input,
            "success": False,
            "story_time": 0,
            "image_time": 0,
            "num_images": 0,
            "story_length": 0,
            "error": None
        }
        
        try:
            # Validate input
            validation = input_handler.validate_input(test_input)
            if not validation["valid"]:
                raise ValueError(f"Invalid input: {validation['message']}")
            
            # Generate story
            start_time = time.time()
            story = story_generator.generate_story(test_input)
            story_time = time.time() - start_time
            test_result["story_time"] = story_time
            results["story_generation_times"].append(story_time)
            
            # Calculate story length
            story_length = len(story.split())
            test_result["story_length"] = story_length
            total_story_length += story_length
            
            if verbose:
                print(f"  - Story generated in {story_time:.2f} seconds ({story_length} words)")
            
            # Save story if requested
            if save_results:
                # Extract title
                title_line = story.split('\n')[0]
                title = title_line[2:] if title_line.startswith('# ') else "Test Story"
                
                # Create folder and save story
                folder_path = file_manager.create_story_folder(f"Test_{i}_{title}")
                markdown_path = file_manager.save_story_markdown(story, folder_path)
                
                # Generate image prompts
                image_prompts = image_prompt_creator.extract_scenes(story)
                
                # Generate images
                start_time = time.time()
                image_paths = image_generator.generate_images(image_prompts, folder_path)
                image_time = time.time() - start_time
                test_result["image_time"] = image_time
                results["image_generation_times"].append(image_time)
                
                # Update markdown with images
                if image_paths:
                    file_manager.update_markdown_with_images(markdown_path, image_paths)
                    test_result["num_images"] = len(image_paths)
                    results["total_images_generated"] += len(image_paths)
                
                if verbose:
                    print(f"  - Generated {len(image_paths)} images in {image_time:.2f} seconds")
                    print(f"  - Saved to: {folder_path}")
            
            test_result["success"] = True
            results["successful_tests"] += 1
            print_colored("  - Test passed successfully", "green")
            
        except Exception as e:
            test_result["error"] = str(e)
            results["failed_tests"] += 1
            print_colored(f"  - Test failed: {str(e)}", "red")
            logging.error(f"Test {i} failed: {str(e)}", exc_info=True)
        
        results["test_details"].append(test_result)
        print("")
    
    # Calculate averages
    if results["story_generation_times"]:
        results["average_story_time"] = sum(results["story_generation_times"]) / len(results["story_generation_times"])
    
    if results["image_generation_times"]:
        results["average_image_time"] = sum(results["image_generation_times"]) / len(results["image_generation_times"])
    
    if total_story_length > 0:
        results["average_story_length"] = total_story_length / results["total_tests"]
    
    # Print summary
    print_colored("\n===== Test Results Summary =====\n", "cyan")
    print(f"Total tests: {results['total_tests']}")
    print(f"Successful: {results['successful_tests']}")
    print(f"Failed: {results['failed_tests']}")
    
    if results["story_generation_times"]:
        print(f"Average story generation time: {results['average_story_time']:.2f} seconds")
    
    if results["image_generation_times"]:
        print(f"Average image generation time: {results['average_image_time']:.2f} seconds")
    
    if "average_story_length" in results:
        print(f"Average story length: {results['average_story_length']:.0f} words")
    
    print(f"Total images generated: {results['total_images_generated']}")
    
    return results


if __name__ == "__main__":
    # Run tests with default inputs
    run_tests(save_results=True, verbose=True)
