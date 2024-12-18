from distutils.core import setup

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tratreetra",
    packages=setuptools.find_packages(),
    version="0.1",
    description="Syntactic transfer from more resourced languages: "
                "TRAnslating TREEbanks for Syntactic TRAnsfer.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Anton Alekseev, Alina Tillabaeva",
    author_email="anton.m.alexeyev+kyrgyz@gmail.com",
    url="https://github.com/alexeyev/tratreetra",
    keywords=["natural language processing", "less-resourced languages", "syntax", "universal dependencies"],
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Linguistic"
    ],
    zip_safe=False,
    include_package_data=True,
    python_requires=">=3.11",
)
