"""
Setup script for SmartWebBot v2.0
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = []
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="smartwebbot",
    version="2.0.0",
    author="SmartWebBot Team",
    author_email="team@smartwebbot.com",
    description="Advanced intelligent web automation framework with AI-powered capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/smartwebbot/smartwebbot",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "docs": [
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.2.0",
            "sphinx-autodoc-typehints>=1.22.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "smartwebbot=cli:cli",
        ],
    },
    include_package_data=True,
    package_data={
        "smartwebbot": [
            "config.yaml",
            "templates/*.yaml",
            "plugins/*.py",
        ],
    },
    keywords=[
        "web automation",
        "selenium",
        "ai",
        "machine learning",
        "browser automation",
        "web scraping",
        "rpa",
        "intelligent automation",
        "computer vision",
        "natural language processing"
    ],
    project_urls={
        "Bug Reports": "https://github.com/smartwebbot/smartwebbot/issues",
        "Source": "https://github.com/smartwebbot/smartwebbot",
        "Documentation": "https://smartwebbot.readthedocs.io",
        "Funding": "https://github.com/sponsors/smartwebbot",
    },
)
