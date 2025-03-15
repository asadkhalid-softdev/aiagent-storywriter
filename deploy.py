#!/usr/bin/env python3
"""
Deployment script for the AI Children's Story Generator.
This script packages the application for distribution.
"""
import os
import sys
import shutil
import subprocess
import platform
import zipfile
from datetime import datetime


def clean_build_directories():
    """Clean build and distribution directories."""
    print("Cleaning build directories...")
    
    directories = ["build", "dist", "story_generator.egg-info"]
    
    for directory in directories:
        if os.path.exists(directory):
            shutil.rmtree(directory)
            print(f"Removed: {directory}")
    
    return True


def create_package():
    """Create a Python package."""
    print("\nCreating Python package...")
    
    try:
        subprocess.run([sys.executable, "setup.py", "sdist", "bdist_wheel"], check=True)
        print("Package created successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating package: {e}")
        return False


def create_zip_archive():
    """Create a ZIP archive of the project."""
    print("\nCreating ZIP archive...")
    
    # Generate timestamp for the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"story_generator_{timestamp}.zip"
    
    # Define files and directories to include
    include = [
        "main.py",
        "install.py",
        "requirements.txt",
        "README.md",
        "setup.py",
        "src",
        "config",
        "docs",
        ".gitignore"
    ]
    
    # Define files and directories to exclude
    exclude = [
        "__pycache__",
        "*.pyc",
        "*.pyo",
        "*.pyd",
        ".git",
        ".env",
        "venv",
        "output",
        "logs",
        "build",
        "dist",
        "*.egg-info"
    ]
    
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for item in include:
                if os.path.isfile(item):
                    zipf.write(item)
                elif os.path.isdir(item):
                    for root, dirs, files in os.walk(item):
                        # Skip excluded directories
                        dirs[:] = [d for d in dirs if not any(d == ex or d.endswith(ex) for ex in exclude)]
                        
                        for file in files:
                            # Skip excluded files
                            if not any(file == ex or file.endswith(ex) for ex in exclude):
                                file_path = os.path.join(root, file)
                                zipf.write(file_path)
        
        print(f"ZIP archive created: {zip_filename}")
        return True
    except Exception as e:
        print(f"Error creating ZIP archive: {e}")
        return False


def create_setup_py():
    """Create setup.py file if it doesn't exist."""
    if os.path.exists("setup.py"):
        return True
    
    print("\nCreating setup.py file...")
    
    setup_content = """
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="story_generator",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-powered children's story generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/story-generator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "story-generator=main:main",
        ],
    },
)
"""
    
    try:
        with open("setup.py", "w", encoding="utf-8") as f:
            f.write(setup_content)
        
        print("setup.py file created.")
        return True
    except Exception as e:
        print(f"Error creating setup.py file: {e}")
        return False


def main():
    """Main deployment function."""
    print("=" * 60)
    print("AI Children's Story Generator - Deployment")
    print("=" * 60)
    
    # Create setup.py file
    create_setup_py()
    
    # Clean build directories
    clean_build_directories()
    
    # Create Python package
    create_package()
    
    # Create ZIP archive
    create_zip_archive()
    
    print("\n" + "=" * 60)
    print("Deployment completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
