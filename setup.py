"""
Setup script for the Flask-MVC PDF Embed/Extract API
"""
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name="flask-pdf-embed-extract",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Flask-based API for embedding and extracting PDFs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/flask-pdf-embed-extract",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Flask",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "flask-pdf-service=run:app.run",
        ],
    },
)