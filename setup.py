#!/usr/bin/python3
import sys
from setuptools import setup  # Noooooo

import nbopen_windows


def load_requirements(fname):
    try:
        # for pip >= 10
        from pip._internal.req import parse_requirements
    except ImportError:
        # for pip <= 9.0.3
        from pip.req import parse_requirements

    reqs = parse_requirements(fname, session="nbopen_windows")
    return [str(ir.req) for ir in reqs]


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='nbopen_windows',
    version=nbopen_windows.__version__,
    author='Zoynels',
    author_email="zoynels@gmail.com",
    url="https://github.com/zoynels/nbopen",
    packages=['nbopen_windows'],
    description="Opens ipynb files on click. Reuses existing jupyter instance if possible. Work only in Windows.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Windows",
    ],
    license="MIT License",
    zip_safe=False,
    keywords=['jupyter', 'notebook', 'ipynb'],
    install_requires=load_requirements("requirements.txt"), 
)

if sys.platform == 'win32':
    print('Writing to registry...', end='')
    import nbopen_windows.install_win
    print('done')
