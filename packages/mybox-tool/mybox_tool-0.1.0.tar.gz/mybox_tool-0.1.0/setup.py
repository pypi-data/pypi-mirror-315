from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mybox-tool",  
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "pyyaml>=6.0.0",
        "rich>=13.0.0",
        "gitpython>=3.1.0",
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=22.0.0',
            'isort>=5.0.0',
            'flake8>=4.0.0',
            'mypy>=1.0.0',
        ]
    },
    entry_points={
        'console_scripts': [
            'mybox=mybox.cli:cli',
        ],
    },
    author="belief",
    author_email="belief.bian@gmail.com",
    description="A powerful multi-repository management tool for Git projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/beliefgp/mybox",
    project_urls={
        "Bug Tracker": "https://github.com/beliefgp/mybox/issues",
        "Documentation": "https://github.com/beliefgp/mybox/tree/main/docs",
        "Source Code": "https://github.com/beliefgp/mybox",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control :: Git",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    keywords="git repository management tool workspace",
)
