"""
Module for handling and validating user input for story generation.
"""
import re
import sys


class InputHandler:
    def __init__(self):
        self.min_length = 10
        self.max_length = 200
        self.forbidden_words = [
            "violent", "kill", "murder", "blood", "gore", "death", 
            "explicit", "sexual", "adult", "nsfw"
        ]

    def get_story_prompt(self):
        """
        Get a story prompt from the user and validate it.
        
        Returns:
            str: Validated story prompt
        """
        print("\n=== AI Children's Story Generator ===")
        print("Please describe the story you'd like to create.")
        print(f"Your description should be between {self.min_length} and {self.max_length} characters.")
        print("Example: 'A friendly dragon who helps children learn about recycling'")
        
        while True:
            try:
                user_input = input("\nYour story idea: ").strip()
                
                # Validate input
                validation_result = self.validate_input(user_input)
                
                if validation_result["valid"]:
                    return user_input
                else:
                    print(f"Input error: {validation_result['message']}")
                    print("Please try again.")
            
            except KeyboardInterrupt:
                print("\nExiting program.")
                sys.exit(0)
    
    def validate_input(self, user_input):
        """
        Validate the user input based on predefined criteria.
        
        Args:
            user_input (str): The user's story prompt
            
        Returns:
            dict: Validation result with 'valid' boolean and 'message' string
        """
        # Check input length
        if len(user_input) < self.min_length:
            return {
                "valid": False,
                "message": f"Input is too short. Minimum {self.min_length} characters required."
            }
        
        if len(user_input) > self.max_length:
            return {
                "valid": False,
                "message": f"Input is too long. Maximum {self.max_length} characters allowed."
            }
        
        # Check for forbidden words
        for word in self.forbidden_words:
            if re.search(r'\b' + re.escape(word) + r'\b', user_input.lower()):
                return {
                    "valid": False,
                    "message": f"Input contains inappropriate content ('{word}'). Please provide a child-friendly story idea."
                }
        
        # Input is valid
        return {"valid": True, "message": "Input is valid"}


if __name__ == "__main__":
    # Test the input handler
    handler = InputHandler()
    prompt = handler.get_story_prompt()
    print(f"Validated prompt: {prompt}")
