from setuptools import setup, find_packages

setup(
    name="chapagol",
    version="0.1.0",
    description="A demo CLI tool to show dirs and files on current directory",
    author="José Schafer",
    author_email="joseignacio.schafer@gmail.com",
    packages=find_packages(),
    install_requires=[
        "typer[all]",  # Include Typer and its dependencies
    ],
    entry_points={
        "console_scripts": [
            "lest=lest.cli:app",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)


