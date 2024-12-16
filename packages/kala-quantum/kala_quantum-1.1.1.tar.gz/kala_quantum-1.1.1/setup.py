
from setuptools import setup, find_packages

setup(
    name="kala_quantum",
    version="1.1.1",
    author="Your Name",
    author_email="your.email@example.com",
    description="A library for quantum-enhanced AI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/username/kala_quantum",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "numpy",
        "torch",
        "tqdm",
        "termcolor",
    ],
)
