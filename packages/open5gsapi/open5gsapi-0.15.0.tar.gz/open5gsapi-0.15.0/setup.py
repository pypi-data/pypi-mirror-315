from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="open5gsapi",
    version="0.15.0", 
    author="Ashwin",
    author_email="f20200893@pilani.bits-pilani.ac.in",
    description="A Python API for interacting with Open5GS components",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ashwinsathish/open5gsapi",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests",
        "pyyaml",
    ],
)