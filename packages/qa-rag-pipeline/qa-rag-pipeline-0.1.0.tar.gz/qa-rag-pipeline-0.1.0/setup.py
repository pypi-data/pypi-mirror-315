from setuptools import setup, find_packages

setup(
    name="qa-rag-pipeline",          # Package name
    version="0.1.0",                 # Initial version
    description="A QA pipeline with RAG capabilities using OpenAI and FAISS",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Tarun",
    author_email="gangadhartarun21@gmail.com ",# Single Python module
    install_requires=[
        "sqlite3",
        "openai",
        "sentence-transformers",
        "numpy",
        "faiss-cpu",
        "datasets",
        "transformers",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
