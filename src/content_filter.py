"""
Module for filtering and ensuring child-appropriate content in stories and images.
"""
import re
import logging
import sys
from pathlib import Path
from openai import OpenAI

# Add project root to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from config.config import OPENAI_API_KEY, STORY_MODEL


class ContentFilter:
    def __init__(self):
        """Initialize the content filter."""
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = STORY_MODEL
        
        # Define inappropriate content patterns
        self.inappropriate_patterns = [
            r'\b(kill|murder|dead|death|die|dying|blood|bloody|gore|violent|violence)\b',
            r'\b(sex|sexual|sexy|nude|naked|explicit|porn|adult|nsfw)\b',
            r'\b(drug|drugs|alcohol|drunk|cigarette|smoking|weed|cocaine|heroin)\b',
            r'\b(gun|guns|weapon|weapons|knife|knives|shoot|shooting)\b',
            r'\b(swear|damn|hell|ass|crap|shit|fuck|bitch|bastard)\b'
        ]
        
        # Define replacement words for common inappropriate terms
        self.replacements = {
            'kill': 'stop',
            'die': 'go away',
            'dead': 'gone',
            'blood': 'water',
            'gun': 'tool',
            'weapon': 'item',
            'knife': 'utensil',
            'shoot': 'point',
            'hell': 'heck',
            'damn': 'darn',
            'ass': 'donkey',
            'crap': 'stuff',
        }
    
    def check_story_content(self, story_text):
        """
        Check if story content is appropriate for children.
        
        Args:
            story_text (str): The story text to check
            
        Returns:
            dict: Results of the content check
        """
        # Check for inappropriate patterns
        issues = []
        for pattern in self.inappropriate_patterns:
            matches = re.finditer(pattern, story_text, re.IGNORECASE)
            for match in matches:
                issues.append({
                    "word": match.group(),
                    "context": story_text[max(0, match.start() - 20):min(len(story_text), match.end() + 20)],
                    "position": match.start()
                })
        
        # Use AI to check for subtle inappropriate content
        ai_check_result = self._ai_content_check(story_text)
        
        result = {
            "is_appropriate": len(issues) == 0 and ai_check_result["is_appropriate"],
            "pattern_issues": issues,
            "ai_check": ai_check_result
        }
        
        logging.info(f"Content check completed: {'PASS' if result['is_appropriate'] else 'FAIL'}")
        if not result["is_appropriate"]:
            logging.warning(f"Found {len(issues)} inappropriate pattern matches")
        
        return result
    
    def filter_story_content(self, story_text):
        """
        Filter inappropriate content from story text.
        
        Args:
            story_text (str): The story text to filter
            
        Returns:
            str: Filtered story text
        """
        # Replace inappropriate words
        filtered_text = story_text
        for word, replacement in self.replacements.items():
            pattern = r'\b' + re.escape(word) + r'\b'
            filtered_text = re.sub(pattern, replacement, filtered_text, flags=re.IGNORECASE)
        
        # Check if further AI filtering is needed
        check_result = self.check_story_content(filtered_text)
        if not check_result["is_appropriate"]:
            # Use AI to rewrite problematic sections
            filtered_text = self._ai_content_filter(filtered_text, check_result)
        
        return filtered_text
    
    def filter_image_prompt(self, prompt):
        """
        Filter and enhance image prompt to ensure child-appropriate content.
        
        Args:
            prompt (str): The image prompt to filter
            
        Returns:
            str: Filtered and enhanced image prompt
        """
        # Replace inappropriate words
        filtered_prompt = prompt
        for word, replacement in self.replacements.items():
            pattern = r'\b' + re.escape(word) + r'\b'
            filtered_prompt = re.sub(pattern, replacement, filtered_prompt, flags=re.IGNORECASE)
        
        # Add safety instructions
        safety_instructions = (
            "Create a child-friendly, G-rated illustration suitable for young children. "
            "Use bright, cheerful colors and a non-threatening style. "
            "Ensure all content is age-appropriate for children ages 4-10. "
        )
        
        # Check if the prompt already has style instructions
        if "style:" in filtered_prompt.lower() or "style=" in filtered_prompt.lower():
            # Insert safety instructions before style instructions
            parts = filtered_prompt.split("Style:", 1) if "Style:" in filtered_prompt else filtered_prompt.split("style:", 1)
            enhanced_prompt = parts[0] + safety_instructions + "Style:" + parts[1]
        else:
            # Add safety instructions and style guidance
            enhanced_prompt = safety_instructions + filtered_prompt + " Style: children's book illustration, colorful, whimsical."
        
        return enhanced_prompt
    
    def _ai_content_check(self, text):
        """
        Use AI to check for subtle inappropriate content.
        
        Args:
            text (str): The text to check
            
        Returns:
            dict: Results of the AI content check
        """
        system_prompt = """
        You are a content moderator for children's stories. Your task is to analyze a story and determine 
        if it contains any content that would be inappropriate for children ages 4-10.
        
        Check for:
        1. Violence or scary content
        2. Adult themes or sexual content
        3. Inappropriate language
        4. Harmful stereotypes or prejudice
        5. Dangerous behaviors children might imitate
        
        Return a JSON object with the following fields:
        - is_appropriate: boolean (true if appropriate, false if not)
        - issues: array of specific issues found (empty if none)
        - explanation: brief explanation of your decision
        """
        
        user_prompt = f"""
        Please analyze this children's story for age-appropriateness:
        
        {text}
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
            
            import json
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            logging.error(f"Error in AI content check: {str(e)}")
            return {
                "is_appropriate": False,
                "issues": ["Error performing AI content check"],
                "explanation": f"Error: {str(e)}"
            }
    
    def _ai_content_filter(self, text, check_result):
        """
        Use AI to rewrite problematic sections of text.
        
        Args:
            text (str): The text to filter
            check_result (dict): Results from content check
            
        Returns:
            str: Filtered text
        """
        system_prompt = """
        You are an expert children's content editor. Your task is to rewrite sections of a children's story 
        to make them age-appropriate while maintaining the story's meaning and flow.
        
        Rewrite the story to:
        1. Remove or replace any inappropriate content
        2. Use child-friendly language
        3. Maintain the original story's message and theme
        4. Keep the same characters and basic plot
        5. Ensure the story remains engaging and educational
        
        Return ONLY the rewritten story, with no explanations or notes.
        """
        
        # Create a prompt that highlights the issues
        issue_descriptions = []
        for issue in check_result.get("pattern_issues", []):
            issue_descriptions.append(f"- '{issue['word']}' in context: \"{issue['context']}\"")
        
        for issue in check_result.get("ai_check", {}).get("issues", []):
            if isinstance(issue, str):
                issue_descriptions.append(f"- {issue}")
        
        user_prompt = f"""
        Please rewrite this children's story to make it age-appropriate for children ages 4-10.
        
        The following issues need to be addressed:
        {chr(10).join(issue_descriptions)}
        
        Original story:
        {text}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            filtered_text = response.choices[0].message.content.strip()
            logging.info("Successfully filtered story content using AI")
            return filtered_text
            
        except Exception as e:
            logging.error(f"Error in AI content filtering: {str(e)}")
            # Fall back to basic filtering
            return text


if __name__ == "__main__":
    # Configure basic logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Test the ContentFilter
    filter = ContentFilter()
    
    test_story = """
    # The Adventure in the Forest
    
    Once upon a time, there was a brave little girl named Lily. She loved exploring the forest behind her house.
    
    One day, Lily found a small knife on the ground. She picked it up and put it in her pocket, thinking it might be useful.
    
    As she walked deeper into the forest, she saw a wounded bird. "Oh no, there's blood on its wing!" she said.
    
    Lily decided to help the bird. She used the knife to cut a piece of her handkerchief and made a small bandage for the bird.
    
    The bird thanked her and flew away. Lily was happy she could help, but she knew she should give the knife to her parents when she got home.
    """
    
    check_result = filter.check_story_content(test_story)
    print("Content Check Result:")
    print(f"Appropriate: {check_result['is_appropriate']}")
    print("Issues found:")
    for issue in check_result["pattern_issues"]:
        print(f"- '{issue['word']}' in context: \"{issue['context']}\"")
    
    filtered_story = filter.filter_story_content(test_story)
    print("\nFiltered Story:")
    print(filtered_story)
    
    test_prompt = "A little girl finding a knife and using it to help a bird with blood on its wing"
    filtered_prompt = filter.filter_image_prompt(test_prompt)
    print("\nFiltered Image Prompt:")
    print(filtered_prompt)
