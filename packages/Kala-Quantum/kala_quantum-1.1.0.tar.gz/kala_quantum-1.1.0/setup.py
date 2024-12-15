from setuptools import setup, find_packages

# Read the contents of the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="Kala-Quantum",
    version="1.1.0",
    author="N V R K SAI KAMESH YADAVALLY",
    author_email="saikamesh.y@gmail.com",
    description="A quantum-powered chatbot framework leveraging quantum state manipulation for advanced conversational capabilities.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kalasaikamesh944/Kala_Quantum.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy",
        "torch",
        "tqdm",
        "termcolor",
    ],
    entry_points={
        'console_scripts': [
            'kala-quantum=kala_quantum.cli:main',  # Adjust this if you provide a CLI tool
        ],
    },
    include_package_data=True,
)
