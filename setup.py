#!/usr/bin/python3
import sys
from setuptools import setup  # Noooooo

import nbopen


def load_requirements(fname):
    try:
        # for pip >= 10
        from pip._internal.req import parse_requirements
    except ImportError:
        # for pip <= 9.0.3
        from pip.req import parse_requirements

    reqs = parse_requirements(fname, session="nbopen")
    return [str(ir.req) for ir in reqs]

setup(name='nbopen',
      version=nbopen.__version__,
      description="Open a notebook from the command line in the best available server",
      author='Thomas Kluyver',
      author_email="thomas@kluyver.me.uk",
      url="https://github.com/takluyver/nbopen",
      install_requires=load_requirements("requirements.txt"), 
)

if sys.platform == "win32":
    import nbopen.install_win
elif (sys.platform == "linux") or (sys.platform == "linux2"):
    import nbopen.install_xdg
