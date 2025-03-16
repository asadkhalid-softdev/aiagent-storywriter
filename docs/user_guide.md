# User Guide

Welcome to the AI Children's Story Generator! This guide will help you create wonderful stories for children with the help of AI.

## Getting Started

### Installation

Before using the application, make sure you have:

1. Python 3.8 or higher installed
2. An OpenAI API key

Follow these steps to install the application:

1. Clone or download the repository
2. Create a virtual environment:

# User Guide

Welcome to the AI Children's Story Generator! This guide will help you create wonderful stories for children with the help of AI.

## Getting Started

### Installation

Before using the application, make sure you have:

1. Python 3.8 or higher installed
2. An OpenAI API key

Follow these steps to install the application:

1. Clone or download the repository
2. Create a virtual environment:
```
python -m venv venv
venv\Scripts\activate # On Windows
source venv/bin/activate # On macOS/Linux
```

3. Install dependencies:
`pip install -r requirements.txt`

4. Create a `.env` file with your OpenAI API key:

OPENAI_API_KEY=your_openai_api_key_here


### Basic Usage

To generate a story:

1. Open a terminal or command prompt
2. Navigate to the project directory
3. Run the application:
python main.py

4. When prompted, enter a story idea or theme
5. Wait while the AI generates your story and images
6. Find your completed story in the `output` directory

## Creating Great Stories

### Crafting Effective Prompts

The quality of your story depends on the prompt you provide. Here are some tips for creating effective prompts:

- **Be specific**: "A friendly dragon who teaches children about recycling" is better than "A story about a dragon"
- **Include characters**: Mention main characters in your prompt
- **Suggest a theme**: Educational themes work well for children's stories
- **Consider age range**: Specify if you want the story for younger or older children
- **Mention setting**: Include where the story takes place

Examples of good prompts:
- "A curious little girl and her cat discover a magical garden in their backyard"
- "A group of animal friends learn about teamwork while building a treehouse"
- "A shy robot goes to school for the first time and makes new friends"

### Customizing Your Story

You can customize various aspects of your story using command-line options:

- Change the number of images:
`python main.py --images 6`


- Adjust the creativity level:
`python main.py --temperature 0.8`

(Higher values = more creative but potentially less coherent)

- Optimize prompts for better quality:
`python main.py --optimize`

## Managing Your Stories

### Finding Your Stories

All generated stories are saved in the `output` directory, with each story in its own folder. The folder name includes the story title and a timestamp.

To list all your stories:
`python main.py --list-stories`

### Story Format

Stories are saved in Markdown format (.md), which can be:
- Viewed in any text editor
- Rendered with proper formatting in applications that support Markdown
- Converted to other formats like PDF or HTML using tools like Pandoc

Each story includes:
- A title
- The story text
- Embedded images at appropriate points in the story

### Sharing Your Stories

To share your stories:

1. Find the story folder in the `output` directory
2. The .md file contains the story text with references to the images
3. The images are stored as separate files in the same folder
4. You can share the entire folder, or convert the Markdown to PDF for easier sharing

To convert to PDF (requires Pandoc):
`pandoc output/your_story_folder/story.md -o story.pdf --pdf-engine=xelatex`

## Troubleshooting

### Common Issues

**The application can't find my API key**
- Make sure you've created a `.env` file in the root directory
- Check that the API key is correctly formatted without extra spaces

**Story generation is taking too long**
- Story generation typically takes 30-60 seconds
- Image generation can take 10-30 seconds per image
- If it's taking much longer, check your internet connection

**The content doesn't seem appropriate for children**
- The application includes content filtering, but it's not perfect
- Use the `--optimize` flag for better quality control
- Review stories before sharing them with children

**The images don't match the story**
- Try using the `--optimize` flag to improve image prompts
- Consider using more specific story prompts that describe visual elements

### Getting Help

If you encounter issues not covered in this guide:

1. Check the logs in the `logs` directory for error messages
2. Look for similar issues in the project's issue tracker
3. Contact the project maintainers with details about your problem

## Advanced Features

### Content Filtering

The application automatically filters content to ensure it's appropriate for children. This includes:

- Checking for inappropriate words and themes
- Rewriting problematic sections
- Enhancing image prompts with safety instructions

### Prompt Optimization

Enable prompt optimization to improve story quality:

python main.py --optimize

This feature:
- Analyzes story quality and age-appropriateness
- Suggests improvements to prompts
- Optimizes image prompts for better illustrations
- Provides feedback on story strengths and weaknesses

When enabled, you'll see an analysis of your story's quality after generation, including an overall rating and key strengths.

### Verbose Mode

For more detailed information during story generation:

python main.py --verbose

text

Verbose mode shows:
- Time taken for each step of the process
- Details about the image prompts being used
- Information about content filtering if issues are found
- Performance statistics

### Custom Output Directory

Save stories to a specific directory:

python main.py --output "my_stories"

text

This is useful for:
- Organizing stories by theme or recipient
- Keeping stories separate from the default output directory
- Saving stories to a shared or cloud-synced folder

## Tips and Tricks

### Creating Educational Stories

For educational stories:
- Mention the educational topic in your prompt
- Be specific about what you want children to learn
- Consider age-appropriateness of the educational content

Example:
python main.py --prompt "A group of animal friends learn about the water cycle through a rainy day adventure"

text

### Creating Personalized Stories

For personalized stories:
- Include the child's name and interests in the prompt
- Mention specific details that will make the story special
- Consider the child's age and reading level

Example:
python main.py --prompt "A story about a 6-year-old girl named Emma who loves dinosaurs and discovers a dinosaur museum in her dreams"

text

### Creating Series of Stories

To create a series with the same characters:
1. Generate the first story with detailed character descriptions
2. For subsequent stories, reference the characters from the first story
3. Keep copies of your prompts to maintain consistency

Example for a series:
python main.py --prompt "Part 2 of the adventures of Max the magical cat and his friend Lily. In this story, they explore an underwater kingdom."

text

## Feedback and Improvement

Your feedback helps improve the AI Children's Story Generator. After creating stories:

- Note what worked well and what could be improved
- Try different prompts and settings to see what produces the best results
- Share your experiences with the project maintainers

Happy storytelling!