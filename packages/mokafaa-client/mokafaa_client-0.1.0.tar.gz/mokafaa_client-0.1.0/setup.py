from setuptools import setup, find_packages

setup(
    name="mokafaa-client",  # Package name for pip
    version="0.1.0",  # Initial version
    description="A Python client for the Mokafaa loyalty API",  # Short description
    long_description=open("README.md").read(),  # Long description from README
    long_description_content_type="text/markdown",  # Content type for PyPI
    author="Ahmed Abdelrahman",  # Author name
    author_email="ahmad18189@gmail.com",  # Author email
    url="https://github.com/ahmad18189/mokafaa-client",  # Project repository
    packages=find_packages(),  # Automatically discover all packages
    install_requires=[
        "requests"  # Required third-party packages
    ],
    python_requires=">=3.6",  # Minimum Python version
    classifiers=[
        "Development Status :: 4 - Beta",  # Package development status
        "Intended Audience :: Developers",  # Target audience
        "License :: OSI Approved :: MIT License",  # License type
        "Programming Language :: Python :: 3",  # Supported language
        "Programming Language :: Python :: 3.6",  # Minimum Python version
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="API client Mokafaa loyalty",  # Keywords for searchability
    project_urls={
        "Source": "https://github.com/ahmad18189/mokafaa-client",
        "Tracker": "https://github.com/ahmad18189/mokafaa-client/issues",
    },
)

