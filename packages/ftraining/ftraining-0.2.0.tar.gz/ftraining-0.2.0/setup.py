from setuptools import setup, find_packages

setup(
    name="ftraining",            # The name of the module
    version="0.2.0",             # Version of the module
    packages=find_packages(),    # Automatically find packages in the module
    install_requires=[           # List of dependencies for your module
        "torch",
        "transformers",
        "datasets",
        "peft",
        "bitsandbytes",
        "accelerate",
        "trl",
    ],
    author="tuber92svv",          # Replace with your name
    author_email="frredrrttt@gmail.com",  # Replace with your email
    description="A fast LLM training module with QLoRA and GPU support.",  # Short description
    long_description=open('README.md').read(),  # Readme file content
    long_description_content_type="text/markdown",
    classifiers=[                # Classifiers for categorization
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',      # Minimum Python version
)
