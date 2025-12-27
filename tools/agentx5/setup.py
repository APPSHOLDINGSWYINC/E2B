"""
Setup script for AgentX5 Multi-Dump Parser
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8")

setup(
    name="agentx5-multi-dump-parser",
    version="1.0.0",
    description="A powerful data parsing tool that automatically splits multi-format dump files into logical datasets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="E2B Team",
    author_email="support@e2b.dev",
    url="https://github.com/e2b-dev/E2B",
    py_modules=["multi_dump_parser"],
    python_requires=">=3.9",
    install_requires=[
        "pandas>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "agentx5-parser=multi_dump_parser:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Financial",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: Apache Software License",
    ],
    keywords="data-parser financial-data csv json robinhood crypto bitcoin",
)
