#!/usr/bin/env python3
"""Setup ytmdl."""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

if __name__ == '__main__':
    setuptools.setup(
        name="ytmdl",
        version="2019.1.30",
        author="Deepjyoti Barman",
        author_email="deep.barma30@gmail.com",
        description="Youtube Music Downloader",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/deepjyoti30/ytmdl",
        packages=setuptools.find_packages(),
        classifiers=(
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ),
        scripts=['bin/ytmdl'],
        install_requires=[
            'youtube_dl==2019.01.30.1',
            'mutagen==1.40.0',
            'itunespy==1.5.5',
            'requests==2.20.0',
            'colorama==0.3.9',
            'bs4==0.0.1'
        ]
    )
