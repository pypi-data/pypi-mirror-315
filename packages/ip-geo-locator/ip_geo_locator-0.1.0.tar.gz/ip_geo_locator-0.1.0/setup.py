from setuptools import setup, find_packages

setup(
    name="ip-geo-locator",
    version="0.1.0",
    author="ip_finder",
    author_email="your.email@example.com",
    description="A Python SDK for IP Finder",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Three-mavericks/ip_finder_python.git",  # Update with your repo
    packages=find_packages(),
    install_requires=[
        "requests>=2.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

