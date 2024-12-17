# setup.py
from setuptools import setup, find_packages

setup(
    name="mistral-vectordb",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.19.0",
        "faiss-cpu>=1.7.0",
        "requests>=2.25.0",
        "tqdm>=4.65.0",
        "pydantic>=1.8.0",
    ],
    author="Viswanath Veera Krishna Maddinala",
    author_email="veerukhnannan@gmail.com",
    description="High-performance vector database with Mistral AI embeddings support",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/veerakrish/mistral-vectordb",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
)