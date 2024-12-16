from setuptools import setup, find_packages

setup(
    name="pySunda",
    version="0.1.0",
    description="Framework Python pikeun make perintah dina basa Sunda",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Frizqi",
    author_email="fadillahfrizqi22@gmail.com",
    url="https://github.com/FIZ-Dev/pysunda",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
