from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="GitWiz",
    version="1.0.1",  # Increment version if re-uploading to PyPI
    packages=find_packages(),
    install_requires=[
        "gitpython",
        "colorama",
        "pyfiglet",
        "ollama"
    ],
    entry_points={
        "console_scripts": [
            "gitwiz=GitWiz.cli:main"  # Ensure your CLI main function is in GitWiz/cli.py
        ]
    },
    author="Ajinkya",
    description="A Git automation tool with an AI-powered README generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache-2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
