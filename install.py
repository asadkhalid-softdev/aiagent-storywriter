#!/usr/bin/env python3
"""
Installation script for the AI Children's Story Generator.
This script sets up the environment, installs dependencies, and configures the application.
"""
import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.8 or higher."""
    required_version = (3, 8)
    current_version = sys.version_info
    
    if current_version < required_version:
        print(f"Error: Python {required_version[0]}.{required_version[1]} or higher is required.")
        print(f"Current version: Python {current_version[0]}.{current_version[1]}.{current_version[2]}")
        return False
    
    print(f"Python version check passed: {current_version[0]}.{current_version[1]}.{current_version[2]}")
    return True


def create_virtual_environment():
    """Create a virtual environment."""
    print("\nCreating virtual environment...")
    
    # Check if venv already exists
    if os.path.exists("venv"):
        response = input("Virtual environment already exists. Recreate? (y/n): ")
        if response.lower() == 'y':
            shutil.rmtree("venv")
        else:
            print("Using existing virtual environment.")
            return True
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("Virtual environment created successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment: {e}")
        return False


def install_dependencies():
    """Install dependencies from requirements.txt."""
    print("\nInstalling dependencies...")
    
    # Determine the pip executable path based on the OS
    if platform.system() == "Windows":
        pip_path = os.path.join("venv", "Scripts", "pip")
    else:
        pip_path = os.path.join("venv", "bin", "pip")
    
    try:
        # Upgrade pip
        subprocess.run([pip_path, "install", "--upgrade", "pip"], check=True)
        
        # Install requirements
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
        
        print("Dependencies installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False


def setup_api_key():
    """Set up the OpenAI API key."""
    print("\nSetting up OpenAI API key...")
    
    # Check if .env file already exists
    if os.path.exists(".env"):
        response = input(".env file already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Keeping existing .env file.")
            return True
    
    # Get API key from user
    api_key = input("Enter your OpenAI API key: ").strip()
    
    if not api_key:
        print("No API key provided. You can add it later to the .env file.")
        return False
    
    # Save to .env file
    try:
        with open(".env", "w") as f:
            f.write(f"OPENAI_API_KEY={api_key}\n")
        
        print("API key saved to .env file.")
        return True
    except Exception as e:
        print(f"Error saving API key: {e}")
        return False


def create_directories():
    """Create necessary directories."""
    print("\nCreating project directories...")
    
    directories = ["output", "logs"]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")
    
    return True


def print_activation_instructions():
    """Print instructions for activating the virtual environment."""
    print("\n" + "=" * 60)
    print("Installation completed!")
    print("=" * 60)
    print("\nTo activate the virtual environment:")
    
    if platform.system() == "Windows":
        print("    venv\\Scripts\\activate")
    else:
        print("    source venv/bin/activate")
    
    print("\nTo run the application:")
    print("    python main.py")
    print("\nFor more information, see the documentation in the docs directory.")
    print("=" * 60)


def main():
    """Main installation function."""
    print("=" * 60)
    print("AI Children's Story Generator - Installation")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Set up API key
    setup_api_key()
    
    # Create directories
    create_directories()
    
    # Print activation instructions
    print_activation_instructions()


if __name__ == "__main__":
    main()
