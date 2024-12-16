from setuptools import setup, find_packages

setup(
    name="dtr_utils",  # Package name
    version="0.1.0",  # Version
    description="Utilities for Decoding Time RAG (DTR) tasks",  # Short description
    author="Rajarshi Roy",  # Your name
    author_email="royrajarshi0123@gmail.com",  # Your email
    # url="https://github.com/yourusername/dtr_utils",  # Repository URL
    packages=find_packages(),  # Automatically find sub-packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # Minimum Python version
    install_requires=[
        "torch==1.12.0",  # For PyTorch support
        "transformers==4.30.0",  # For Hugging Face models (GPT-2, Llama, etc.)
        "accelerate==0.19.0",  # For distributed model training
        "numpy==1.23.0",  # For numerical operations
        "tqdm==4.64.0",  # For progress bars
        "nltk>=3.6.3",  # For Natural Language Toolkit (tokenization, etc.)
        "sentence-transformers>=2.2.0",  # For SentenceTransformer models
        "scikit-learn>=0.24.2",  # For CountVectorizer and other features
        "matplotlib>=3.4.0",  # For plotting
        "seaborn>=0.11.0",  # For statistical data visualization
        "scipy>=1.6.0",  # For entropy and other statistical functions
        "anytree>=2.8.0",  # For tree data structures
        "graphviz>=0.16",  # For graph visualization
        "stanza>=1.4.0",  # For NLP processing
        "spacy>=3.0.0",  # For spaCy NLP toolkit
        "beautifulsoup4>=4.9.3",  # For HTML parsing (BeautifulSoup)
        "googlesearch-python==1.2.5",  # For Google search functionality
        "requests>=2.25.1",  # For handling HTTP requests
        "lxml>=4.6.3",  # For XML and HTML parsing
        "pandas>=1.3.0",  # For handling data structures (e.g., DataFrames)
    ],
)
