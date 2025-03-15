"""
Module for optimizing and refining prompts for story and image generation.
"""
import json
import logging
import os
from openai import OpenAI
import sys
from pathlib import Path
import time

# Add project root to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from config.config import OPENAI_API_KEY, STORY_MODEL


class PromptOptimizer:
    def __init__(self):
        """Initialize the prompt optimizer."""
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = STORY_MODEL
    
    def analyze_story_quality(self, story_text, original_prompt):
        """
        Analyze the quality of a generated story and suggest prompt improvements.
        
        Args:
            story_text (str): The generated story text
            original_prompt (str): The original prompt used to generate the story
            
        Returns:
            dict: Analysis results with quality metrics and suggested improvements
        """
        system_prompt = """
        You are an expert children's literature analyst. Your task is to analyze a children's story 
        and provide detailed feedback on its quality, appropriateness, and engagement level for children.
        
        Analyze the following aspects:
        1. Age-appropriateness (vocabulary, themes, complexity)
        2. Narrative structure (beginning, middle, end)
        3. Character development
        4. Educational value
        5. Engagement and entertainment value
        6. Language quality and readability
        7. Emotional impact and positive messaging
        
        Also suggest specific improvements to the original prompt that would result in a better story.
        
        Return your analysis as a JSON object with the following fields:
        - overall_rating: A score from 1-10
        - strengths: List of story strengths
        - weaknesses: List of story weaknesses
        - age_range: Appropriate age range for the story
        - improved_prompt: A refined version of the original prompt
        """
        
        user_prompt = f"""
        Original Prompt: "{original_prompt}"
        
        Generated Story:
        {story_text}
        
        Please analyze this children's story and provide detailed feedback.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            analysis = json.loads(response.choices[0].message.content)
            logging.info(f"Story quality analysis completed with overall rating: {analysis.get('overall_rating', 'N/A')}")
            return analysis
            
        except Exception as e:
            logging.error(f"Error analyzing story quality: {str(e)}")
            return {
                "overall_rating": 0,
                "strengths": [],
                "weaknesses": ["Error analyzing story"],
                "age_range": "unknown",
                "improved_prompt": original_prompt,
                "error": str(e)
            }
    
    def optimize_image_prompts(self, story_text, image_prompts):
        """
        Optimize image prompts for better quality and relevance to the story.
        
        Args:
            story_text (str): The story text
            image_prompts (list): The original image prompts
            
        Returns:
            list: Optimized image prompts
        """
        system_prompt = """
        You are an expert in creating prompts for AI image generation, specializing in children's book illustrations.
        Your task is to analyze a set of image prompts for a children's story and optimize them for:
        
        1. Visual clarity and specificity
        2. Child-friendliness and appropriateness
        3. Artistic style consistency
        4. Emotional resonance with the story
        5. Diversity of scenes and perspectives
        6. Technical effectiveness for AI image generation
        
        For each prompt, provide an optimized version that will result in better illustrations.
        
        Return your analysis as a JSON array of optimized prompts.
        """
        
        user_prompt = f"""
        Story Text:
        {story_text}
        
        Original Image Prompts:
        {json.dumps(image_prompts, indent=2)}
        
        Please optimize these image prompts for better quality and relevance to the story.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Handle different possible response formats
            if isinstance(result, list):
                optimized_prompts = result
            elif "prompts" in result:
                optimized_prompts = result["prompts"]
            elif "optimized_prompts" in result:
                optimized_prompts = result["optimized_prompts"]
            else:
                # Try to find any array in the response
                for key, value in result.items():
                    if isinstance(value, list):
                        optimized_prompts = value
                        break
                else:
                    # If no array found, return the original prompts
                    return image_prompts
            
            logging.info(f"Optimized {len(optimized_prompts)} image prompts")
            return optimized_prompts
            
        except Exception as e:
            logging.error(f"Error optimizing image prompts: {str(e)}")
            return image_prompts
    
    def save_optimization_results(self, analysis, original_prompt, story_text, output_dir):
        """
        Save optimization results to a file for future reference.
        
        Args:
            analysis (dict): Analysis results
            original_prompt (str): Original story prompt
            story_text (str): Generated story text
            output_dir (str): Directory to save results
            
        Returns:
            str: Path to the saved file
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Create filename based on prompt
        import hashlib
        prompt_hash = hashlib.md5(original_prompt.encode()).hexdigest()[:8]
        filename = f"optimization_{prompt_hash}.json"
        filepath = os.path.join(output_dir, filename)
        
        # Prepare data to save
        data = {
            "original_prompt": original_prompt,
            "story_excerpt": story_text[:500] + "..." if len(story_text) > 500 else story_text,
            "analysis": analysis,
            "timestamp": str(time.time())
        }
        
        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        logging.info(f"Saved optimization results to {filepath}")
        return filepath


if __name__ == "__main__":
    # Test the prompt optimizer
    optimizer = PromptOptimizer()
    
    test_story = """
    # The Recycling Dragon
    
    Once upon a time, in a small town nestled between green hills, there lived a friendly dragon named Ember. Unlike the dragons in storybooks, Ember didn't breathe fire to scare people. Instead, he used his warm breath to help the townspeople in many ways.
    
    One day, Ember noticed that the beautiful hills around the town were becoming covered with trash. Plastic bottles, paper, and old toys were scattered everywhere. This made Ember very sad.
    
    "Why are the hills so messy?" Ember asked a little girl named Lily who often came to visit him.
    
    "People throw away too many things," Lily explained. "They don't know how to recycle."
    
    "What's recycling?" asked Ember curiously.
    
    Lily smiled and took Ember's claw. "Come with me. I'll show you!"
    
    Lily taught Ember all about recycling. She showed him how paper could be made into new paper, how plastic bottles could become new things, and how metal cans could be melted and shaped again.
    
    Ember was amazed! "So things don't have to be thrown away forever?" he asked.
    
    "That's right," said Lily. "But many people don't know how to recycle properly, or they think it's too much work."
    
    Ember thought hard. Then his eyes lit up with an idea. "I can help!" he declared.
    
    The next day, Ember and Lily went to the town square. Ember announced his plan to help clean up the hills and teach everyone about recycling.
    
    "I can use my wings to collect trash from hard-to-reach places," said Ember. "And I can use my warm breath to help sort different materials."
    
    The townspeople were excited about Ember's idea. Together, they set up recycling stations around town. Ember used his fire breath to melt down metals for reuse, and his gentle warmth to help dry recycled paper pulp.
    
    Children from the school came to watch and learn. Ember taught them songs about recycling and games to help remember which items went where.
    
    "Plastic in the blue bin, paper in the green! Metal in the red bin, keeps the planet clean!" they would sing as they sorted their trash.
    
    Soon, the hills began to look clean again. The town started a recycling festival, with Ember as the guest of honor. Everyone brought items to recycle and created new, useful things from materials that would have been thrown away.
    
    Lily was proud of her dragon friend. "You've taught everyone that even small actions can make a big difference," she told Ember.
    
    Ember smiled. "And you taught me that learning new things can help solve big problems."
    
    From that day on, the town became famous for being the cleanest, greenest place around, all thanks to a friendly dragon who learned about recycling and shared that knowledge with everyone he met.
    
    And whenever a new family moved to town, the children would excitedly tell them, "Wait until you meet our recycling dragon! He'll show you how to keep our world beautiful!"
    """
    
    test_prompt = "A friendly dragon who helps children learn about recycling"
    
    analysis = optimizer.analyze_story_quality(test_story, test_prompt)
    print(json.dumps(analysis, indent=2))
    
    test_image_prompts = [
        "A friendly red dragon named Ember looking sad at trash-covered hills",
        "Lily teaching Ember about recycling with sorting bins",
        "Ember using his wings to collect trash from hills and his breath to sort materials",
        "Children and Ember at a recycling festival with the cleaned-up town in background"
    ]
    
    optimized_prompts = optimizer.optimize_image_prompts(test_story, test_image_prompts)
    print(json.dumps(optimized_prompts, indent=2))
