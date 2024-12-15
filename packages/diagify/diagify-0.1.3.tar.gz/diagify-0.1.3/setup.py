from setuptools import setup, find_packages

setup(
    name="diagify",
    version="0.1.3",
    packages=find_packages(include=["diagify", "diagify.*"]),
    install_requires=[
        "openai",
        "diagrams",
        "graphviz"
    ],
    entry_points={
        "console_scripts": [
            "diagify=diagify.main:main",
        ],
    },
    author="Alex Minnaar",
    author_email="minnaaralex@gmail.com",
    description="A tool to generate diagrams from natural language using Mingrammer.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/alexminnaar/diagify",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
