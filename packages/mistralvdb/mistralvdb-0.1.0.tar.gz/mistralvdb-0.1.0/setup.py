"""Setup configuration for MistralVDB."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mistralvdb",
    version="0.1.0",
    author="Viswanath Veera Krishna Maddinala",
    author_email="veerukhannann@gmail.com",
    description="A vector database optimized for Mistral AI embeddings with HNSW indexing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/veerakrish/mistralvdb",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Database :: Database Engines/Servers",
    ],
    python_requires=">=3.8",
    install_requires=[
        "mistralai>=1.2.5",
        "numpy>=1.21.0",
        "scikit-learn>=1.0.0",
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "python-multipart>=0.0.5",
        "tenacity>=8.2.3",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.3.0",
            "isort>=5.10.1",
            "flake8>=4.0.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "mistralvdb-server=mistralvdb.cli:run_server",
        ],
    },
)
