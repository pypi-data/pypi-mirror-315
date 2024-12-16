from setuptools import setup, find_packages

setup(
    name="interrail_vision",
    version="0.1.2",
    description="A package for reading images and PDFs via AI-powered vision",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="ShakhCo",
    author_email="shakhzodbeksharipov@outlook.com",
    url="https://github.com/Shakh7/",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pillow",
        "pymupdf",
        "openai",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
