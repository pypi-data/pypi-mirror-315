from setuptools import setup

setup(
    name="jasim_chatbot",  # Package name
    version="0.1.0",  # Version of your package
    author="Jasim Jamil",  # Your name
    description="A simple chatbot package using Hugging Face.",  # Short description
    long_description="This chatbot uses Hugging Face models to generate AI responses.",  # Detailed description
    long_description_content_type="text/plain",  # Format of long description
    py_modules=["jasim_chatbot"],  # List of Python modules to include
    install_requires=[  # Dependencies that need to be installed with the package
        "transformers",  # Hugging Face's transformer library
        "torch",  # PyTorch library for running the models
    ],
    entry_points={  # Define the command to run your chatbot
        "console_scripts": [
            "jasim_chatbot=jasim_chatbot:main",  # Command to start the chatbot
        ]
    },
    python_requires=">=3.6",  # Minimum Python version requirement
)
