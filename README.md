# AI Children's Story Generator

An AI-powered application that generates children's stories with accompanying images based on user input. This tool uses OpenAI's GPT models to create engaging, age-appropriate stories and DALL-E to generate matching illustrations.

## Features

- Generate complete children's stories from simple prompts
- Create matching illustrations for key scenes in the story
- Save stories in Markdown format with embedded images
- Filter content to ensure child-appropriateness
- Optimize prompts for better quality stories and images
- Monitor performance and resource usage

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Basic Usage](#basic-usage)
  - [Command-Line Options](#command-line-options)
  - [Examples](#examples)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Step 1: Clone the repository

git clone https://github.com/yourusername/story-generator.git
cd story-generator

### Step 2: Create a virtual environment

#### On Windows
python -m venv venv
venv\Scripts\activate

#### On macOS/Linux
python -m venv venv
source venv/bin/activate

### Step 3: Install dependencies

pip install -r requirements.txt

### Step 4: Set up your API key

Create a `.env` file in the root directory with your OpenAI API key:

OPENAI_API_KEY=your_openai_api_key_here

## Usage

### Basic Usage

Run the application with the following command:

python main.py

The application will prompt you to enter a story idea. After you provide a prompt, it will:
1. Generate a children's story based on your prompt
2. Create image prompts for key scenes in the story
3. Generate images for those scenes
4. Save the story with embedded images in the output directory

### Command-Line Options

The application supports various command-line options:

usage: main.py [-h] [-p PROMPT] [-i IMAGES] [-o OUTPUT] [-v]
[--log {DEBUG,INFO,WARNING,ERROR}] [--model MODEL]
[--image-model IMAGE_MODEL] [--temperature TEMPERATURE]
[--optimize] [--no-filter] [--test] [--list-stories]
[--version]

AI Children's Story Generator

options:
-h, --help show this help message and exit
-p PROMPT, --prompt PROMPT
Story prompt (if not provided, will prompt interactively)
-i IMAGES, --images IMAGES
Number of images to generate
-o OUTPUT, --output OUTPUT
Custom output directory
-v, --verbose Enable verbose output
--log {DEBUG,INFO,WARNING,ERROR}
Set logging level (default: INFO)

Advanced Options:
--model MODEL Specify GPT model for story generation
--image-model IMAGE_MODEL
Specify model for image generation
--temperature TEMPERATURE
Creativity level (0.0-1.0) for story generation
--optimize Optimize prompts for better quality
--no-filter Disable content filtering
--test Run test suite with sample prompts

Actions:
--list-stories List all generated stories
--version Show version information and exit


### Examples

1. Generate a story with a specific prompt:
python main.py --prompt "A friendly dragon who teaches children about recycling"


2. Generate a story with more images:
python main.py --prompt "A space adventure with talking planets" --images 6


3. Save output to a custom directory:
python main.py --output "my_stories"


4. Enable prompt optimization for better quality:
python main.py --optimize


5. Run the test suite:
python main.py --test


6. List all previously generated stories:
python main.py --list-stories


## Project Structure

```
story_generator/
│
├── main.py # Main entry point for the application
├── requirements.txt # Project dependencies
├── README.md # Project documentation
│
├── config/
│ └── config.py # Configuration settings (API keys, etc.)
│
├── src/
│ ├── input_handler.py # Module for handling user input
│ ├── story_generator.py # Module for generating stories using GPT
│ ├── image_prompt_creator.py # Module for creating image prompts from story
│ ├── image_generator.py # Module for generating images from prompts
│ ├── file_manager.py # Module for file and directory operations
│ ├── utils.py # Utility functions
│ ├── cli.py # Command-line interface
│ ├── content_filter.py # Content filtering for child-appropriateness
│ ├── performance_monitor.py # Performance monitoring and optimization
│ ├── prompt_optimizer.py # Prompt optimization for better quality
│ └── test_app.py # Testing module
│
├── logs/ # Directory for log files
│ └── .gitkeep
│
└── output/ # Directory for storing generated stories and images
└── .gitkeep
```

## Configuration

The application can be configured by editing the `config/config.py` file. Key configuration options include:

- `STORY_MODEL`: The GPT model to use for story generation (default: "gpt-4-turbo")
- `STORY_MAX_TOKENS`: Maximum tokens for story generation (default: 2000)
- `STORY_TEMPERATURE`: Creativity level for story generation (default: 0.7)
- `IMAGE_MODEL`: The model to use for image generation (default: "dall-e-3")
- `IMAGE_SIZE`: Size of generated images (default: "1024x1024")
- `IMAGES_PER_STORY`: Number of images to generate per story (default: 4)

## Advanced Features

### Content Filtering

The application includes a content filter to ensure all stories and images are appropriate for children. This filter:

- Checks for inappropriate words and phrases
- Uses AI to analyze content for subtle inappropriate themes
- Automatically rewrites problematic sections
- Enhances image prompts with safety instructions

To disable content filtering (not recommended for children's stories):

python main.py --no-filter


### Prompt Optimization

The prompt optimizer analyzes generated stories and suggests improvements to prompts for better quality. It:

- Evaluates story quality, age-appropriateness, and engagement
- Optimizes image prompts for better illustrations
- Provides feedback on story strengths and weaknesses

To enable prompt optimization:

python main.py --optimize

### Performance Monitoring

The application includes a performance monitoring system that tracks:

- Operation times for different components
- System resource usage during story generation
- Statistics for optimization opportunities

Performance data is saved in the story's folder under a "performance" directory.

## Troubleshooting

### API Key Issues

If you encounter errors related to the API key:

1. Make sure your `.env` file is in the root directory
2. Verify that your API key is correct and has sufficient credits
3. Check that the API key has access to the required models

### Generation Failures

If story or image generation fails:

1. Check the logs in the `logs` directory for detailed error messages
2. Try using a different model with the `--model` or `--image-model` options
3. Simplify your prompt and try again

### Performance Issues

If the application is running slowly:

1. Use a smaller number of images with the `--images` option
2. Try a faster (though potentially less capable) model
3. Check the performance logs to identify bottlenecks

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.