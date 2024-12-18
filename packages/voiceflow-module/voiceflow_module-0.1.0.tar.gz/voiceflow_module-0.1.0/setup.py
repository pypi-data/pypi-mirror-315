from setuptools import setup, find_packages

setup(
    name="voiceflow_module",
    version="0.1.0",
    author="Alex",
    author_email="Alex@parnidia.com",
    description="A reusable module for uploading files and tables to Voiceflow.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://parnidia.com/en",
    packages=find_packages(),
    classifiers=[                      # Metadata for PyPI
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests",
    ],
)