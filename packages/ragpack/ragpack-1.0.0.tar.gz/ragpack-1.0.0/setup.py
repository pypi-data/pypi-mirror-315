from setuptools import setup, find_packages

setup(
    name="ragpack",
    version="1.0.0",
    description="A Python package for RAG pipelines using OpenAI and FAISS.",
    author="Tarun",
    author_email="gangadhartarun21@gmail.com",
    packages=find_packages(),
    install_requires=[
    'openai==0.28.0',
    'sentence-transformers==3.2.1',
    'faiss-cpu==1.9.0',
    'datasets==3.2.0',
    'transformers==4.46.3',
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
