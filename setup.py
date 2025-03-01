from setuptools import setup, find_packages

setup(
    name="nexus-client",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "grpcio",
        "protobuf",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python client for the Nexus service",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/nexus-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 