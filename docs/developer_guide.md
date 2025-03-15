User Input → Input Handler → Story Generator → Story Text → Image Prompt Creator →
Image Prompts → Image Generator → Images → File Manager → Final Output

text

Additional components like Content Filter and Prompt Optimizer interact with this flow at various points.

## Core Components

### Input Handler

The Input Handler (`src/input_handler.py`) is responsible for:

- Collecting user input via command line
- Validating input for length and appropriateness
- Providing feedback on invalid input

Key methods:
- `get_story_prompt()`: Gets and validates user input
- `validate_input(user_input)`: Checks if input meets requirements

### Story Generator

The Story Generator (`src/story_generator.py`) is responsible for:

- Connecting to OpenAI's API
- Crafting effective prompts for story generation
- Handling API errors and retries
- Formatting the story output

Key methods:
- `generate_story(prompt)`: Generates a story based on the provided prompt

### Image Prompt Creator

The Image Prompt Creator (`src/image_prompt_creator.py`) is responsible for:

- Analyzing story text to identify key scenes
- Creating detailed prompts for image generation
- Ensuring prompts are child-appropriate
- Providing fallback mechanisms if extraction fails

Key methods:
- `extract_scenes(story_text)`: Extracts key scenes for image generation

### Image Generator

The Image Generator (`src/image_generator.py`) is responsible for:

- Connecting to OpenAI's DALL-E API
- Generating images based on prompts
- Handling API errors and retries
- Saving generated images

Key methods:
- `generate_images(image_prompts, story_folder)`: Generates images for the given prompts

### File Manager

The File Manager (`src/file_manager.py`) is responsible for:

- Creating appropriately named folders for stories
- Saving stories in Markdown format
- Organizing images with the story text
- Updating Markdown files to include images

Key methods:
- `create_story_folder(story_title)`: Creates a folder for the story
- `save_story_markdown(story_text, folder_path)`: Saves the story as Markdown
- `update_markdown_with_images(markdown_path, image_paths)`: Updates Markdown with images

## Advanced Components

### Content Filter

The Content Filter (`src/content_filter.py`) is responsible for:

- Checking story content for inappropriate material
- Filtering and replacing inappropriate content
- Enhancing image prompts with safety instructions
- Using AI to rewrite problematic sections

Key methods:
- `check_story_content(story_text)`: Checks if content is appropriate
- `filter_story_content(story_text)`: Filters inappropriate content
- `filter_image_prompt(prompt)`: Enhances image prompts for safety

### Performance Monitor

The Performance Monitor (`src/performance_monitor.py`) is responsible for:

- Tracking operation times
- Monitoring system resource usage
- Collecting performance statistics
- Identifying optimization opportunities

Key methods:
- `start_operation(operation_name)`: Starts tracking an operation
- `end_operation(operation_name)`: Ends tracking an operation
- `get_operation_stats()`: Gets statistics about operations

### Prompt Optimizer

The Prompt Optimizer (`src/prompt_optimizer.py`) is responsible for:

- Analyzing story quality
- Suggesting prompt improvements
- Optimizing image prompts
- Providing feedback on story strengths and weaknesses

Key methods:
- `analyze_story_quality(story_text, original_prompt)`: Analyzes story quality
- `optimize_image_prompts(story_text, image_prompts)`: Optimizes image prompts

## Extending the Application

### Adding New Features

To add a new feature:

1. Identify which component should contain the feature
2. Create a new method or class as needed
3. Update the main.py file to use the new feature
4. Add any new command-line options to cli.py
5. Update the documentation

### Adding New Models

To add support for a new model:

1. Update the config.py file with the new model information
2. Modify the story_generator.py or image_generator.py file as needed
3. Add any new parameters to the command-line interface

### Customizing Prompts

The system prompts used for story and image generation can be customized:

1. In story_generator.py, modify the `system_prompt` variable in the `generate_story` method
2. In image_prompt_creator.py, modify the `system_prompt` variable in the `extract_scenes` method

### Adding New Output Formats

To add support for a new output format:

1. Create a new method in file_manager.py to handle the format
2. Update the main.py file to use the new method
3. Add any new command-line options to cli.py

## Testing

The application includes a testing module (`src/test_app.py`) that can:

- Run the application with various test inputs
- Collect performance metrics
- Identify issues with story or image generation

To run tests:

python main.py --test

text

## Logging

The application uses Python's logging module to log information, warnings, and errors:

- Logs are stored in the `logs` directory
- The log level can be set with the `--log` command-line option
- Log files are named with the current date

To view logs:

cat logs/story_generator_YYYYMMDD.log

text

## Performance Optimization

To optimize performance:

1. Use the Performance Monitor to identify bottlenecks
2. Consider using faster models for less complex stories
3. Implement caching for commonly used prompts
4. Optimize image generation by reducing the number or size of images

## API Usage and Costs

The application uses OpenAI's API, which has associated costs:

- GPT-4 usage for story generation
- DALL-E usage for image generation

To manage costs:

1. Use smaller models when appropriate
2. Reduce the number of images generated
3. Implement caching for repeated operations
4. Monitor your API usage in the OpenAI dashboard