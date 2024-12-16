from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="Gatria",
    version="0.1.0",
    author="Pradyumn Tandon",
    author_email="pradyumn.tandon@hotmail.com",
    description="A comprehensive employee management system with multiple framework adapters",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Canopus-Development/Gatria",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "flask>=2.0.0",
        "django>=4.0.0",
        "sqlalchemy>=1.4.0",
        "pymongo>=4.0.0",
        "aiohttp>=3.8.0",
        "scikit-learn>=1.0.0",
        "tensorflow>=2.0.0",
        "numpy>=1.20.0",
        "pandas>=1.3.0",
    ],
    extras_require={
        'web': [
            'flask>=2.0.0',
            'django>=4.0.0',
            'fastapi>=0.68.0',
            'uvicorn>=0.15.0',
        ],
        'database': [
            'sqlalchemy>=1.4.0',
            'pymongo>=4.0.0',
            'redis>=4.0.0',
        ],
        'async': [
            'aiohttp>=3.8.0',
            'asyncio>=3.4.3',
            'websockets>=10.0',
        ],
        'ml': [
            'scikit-learn>=1.0.0',
            'tensorflow>=2.0.0',
            'torch>=1.9.0',
            'numpy>=1.20.0',
            'pandas>=1.3.0',
        ],
        'dev': [
            'pytest>=6.0.0',
            'black>=21.0.0',
            'isort>=5.0.0',
            'mypy>=0.900',
            'flake8>=3.9.0',
        ],
    }
)
