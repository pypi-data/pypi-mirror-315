from setuptools import setup, find_packages

setup(
    name="textutilsSohaib",  # Library name
    version="0.1.0",  # Initial version
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple library for text transformations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/textutils",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
