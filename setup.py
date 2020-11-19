#!/usr/bin/env python3
"""Setup ytmdl."""

import setuptools
from os import path
from warnings import warn

with open("README.md", "r") as fh:
    long_description = fh.read()

exec(open("ytmdl/__version__.py").read())

req_pkgs = [
            'youtube_dl',
            'mutagen',
            'itunespy',
            'requests',
            'colorama',
            'bs4',
            'downloader-cli',
            'lxml',
            'pyxdg',
            'ffmpeg-python',
            'pysocks',
            'unidecode',
            'youtube_search',
            'pyDes',
            'urllib3',
            'simber'
          ]


extra_features = {
            'noise-clean': ['inaSpeechSegmenter', 'tensorflow']
        }


# Add the distributable files
file_map = [
    ('/etc/bash_completion.d', 'ytmdl.bash'),
    ('/usr/share/zsh/functions/Completion/Unix', 'ytmdl.zsh')
]

data_files = []
for dirname, filename in file_map:
    if not path.exists(filename):
        warn("%s does not exist, skipping." % filename)
    else:
        data_files.append((dirname, [filename]))

params = {
    'data_files': data_files,
}


if __name__ == '__main__':
    setuptools.setup(
        name="ytmdl",
        version=__version__,
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
        python_requires=">=3.*",
        scripts=['bin/ytmdl'],
        install_requires=req_pkgs,
        setup_requires=req_pkgs,
        extras_require=extra_features,
        **params
    )
