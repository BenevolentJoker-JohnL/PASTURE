#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
setup.py

Setup script for installing the PASTURE framework as a Python package.
"""

from setuptools import setup, find_packages
import os

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Define package metadata
setup(
    name="pasture",
    version="1.0.0",
    author="PASTURE Framework Team",
    author_email="your.email@example.com",
    description="PASTURE Framework for AI model orchestration with Ollama",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourrepo/pasture",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "aiohttp>=3.8.0",
        "pydantic>=2.0.0",
        "tenacity>=8.0.0",
    ],
    extras_require={
        "celery": [
            "celery>=5.3.0",
            "redis>=4.5.0",
            "flower>=2.0.0"
        ],
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.3.0"
        ],
        "all": [
            "celery>=5.3.0",
            "redis>=4.5.0",
            "flower>=2.0.0",
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.3.0"
        ]
    },
    include_package_data=True,
    package_data={
        "pasture": ["config/*.json"],
    },
)
