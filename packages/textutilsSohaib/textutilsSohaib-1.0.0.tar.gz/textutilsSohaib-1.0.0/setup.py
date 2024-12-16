from setuptools import setup, find_packages

setup(
    name="textutilsSohaib",  # Exact name of the package
    version="1.0.0",  # Version 1.0.0
    description="A simple text utility package providing text manipulation functions",
    long_description=open("README.md").read(),  # A detailed description (make sure README.md exists)
    long_description_content_type="text/markdown",  # Markdown format for PyPI
    author="Muhammad Sohaib Hassan",  # Your name
    author_email="muhammadsohaibhassan3@gmail.com",  # Your email
    url="https://github.com/MuhammadSohaibHassan/textutilsSohaib",  # URL to your repository (change to actual URL)
    packages=find_packages(),  # Automatically detects the textutilsSohaib folder
    classifiers=[  # PyPI classifiers
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version
)
