# setup.py
from setuptools import setup, find_packages

setup(
    name="Kala_Quantum",
    version="0.0.0",
    description="A quantum-powered chatbot framework with quantum state manipulation capabilities.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="N V R K SAI KAMESH SHARMA",
    author_email="saikamesh.y@gmail.com",
    url="https://github.com/Kalasaikamesh944/Kala_Quantum.git",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.20.0",
        "tqdm>=4.50.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
