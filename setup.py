#!/usr/bin/env python3
"""Setup ytmdl."""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

if __name__ == '__main__':
    setuptools.setup(
        name="ytmdl",
        version="2019.10.8",
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
            'youtube_dl',
            'mutagen',
            'itunespy',
            'requests',
            'colorama',
            'bs4'
        ]
    )
