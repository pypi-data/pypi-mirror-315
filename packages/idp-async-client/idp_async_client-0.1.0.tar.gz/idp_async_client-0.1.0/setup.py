from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="idp-async-client",
    version="0.1.0",
    author="Sifat Ibna Amin",
    author_email="sifatibna.amin9@gmail.com",
    description="An async Python client for Keycloak authentication",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SifatIbna/idp-async-client.git",
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
        "Programming Language :: Python :: 3.11",
        "Topic :: Security",
        "Framework :: AsyncIO",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "PyJWT>=2.0.0",
        "cryptography>=3.4.0",
        "aiohttp>=3.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-asyncio>=0.14.0",
            "pytest-cov>=2.0.0",
            "black>=21.0.0",
            "isort>=5.0.0",
            "mypy>=0.900",
            "flake8>=3.9.0",
        ],
    }
)