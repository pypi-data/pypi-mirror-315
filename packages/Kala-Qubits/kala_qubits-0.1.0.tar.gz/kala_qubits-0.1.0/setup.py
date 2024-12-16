# setup.py

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="Kala_Qubits",
    version="0.1.0",
    description="A lightweight quantum circuit simulator with PyTorch backend",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="N V R K SAI KAMESH YADAVALLI",
    author_email="saikamesh.y@gmail.com",
    url="https://github.com/Kalasaikamesh944/Qubits",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.20.0",
        "torch>=1.10.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
