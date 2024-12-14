from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Basic aoc utils'
LONG_DESCRIPTION = 'Library for basic Advent of Code Utilities'

setup(
    name="kryptikkaocutils",
    version=VERSION,
    author="Lars Junker",
    author_email="larsjunker92@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    keywords=['python', 'aoc', 'aoc-utils'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)