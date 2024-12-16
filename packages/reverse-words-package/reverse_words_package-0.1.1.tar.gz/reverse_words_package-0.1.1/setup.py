from setuptools import setup, find_packages # type: ignore

setup(
    name="reverse-words-package",
    version="0.1.1",
    author="Ваше Ім'я",
    author_email="your.email@example.com",
    description="A Python package to reverse words in a string while preserving non-alphabetic characters.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your_username/reverse_words_package",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
