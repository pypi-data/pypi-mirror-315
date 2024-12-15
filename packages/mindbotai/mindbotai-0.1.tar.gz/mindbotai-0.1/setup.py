# setup.py

from setuptools import setup, find_packages

setup(
    name="mindbotai",  # Name of the package
    version="0.1",
    packages=find_packages(),  # Automatically find packages in the mindbot directory
    install_requires=[
        "google-generativeai",  # Add the required dependencies
        "httpx",
    ],
    description="MindBot AI Functions Package",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Ahmed Helmy Ali Eletr",
    author_email="ahmedhelmyali.dev@gmail.com",
    url="https://github.com/AetherMind-Ai/mindbotlibrary",  # Replace with your repository URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
