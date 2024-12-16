from setuptools import setup, find_packages

setup(
    name="Kala_Quantum",
    version="1.0.1",
    description="A framework for hybrid quantum-classical AI models",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="N V R K SAI KAMESH YADAVALLI",
    author_email="saikamesh.y@gmail.com",
    url="https://github.com/Kalasaikamesh944/Kala_Quantum",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "torch>=1.10.0",
        "tqdm>=4.62.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
