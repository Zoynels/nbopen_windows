Open notebooks from the command line

nbopen looks for the nearest running notebook server - if it finds one, it
opens a web browser to that notebook. If not, it starts a new notebook server
in that directory.

Installation::

    python -m pip install nbopen_windows
    python -m pip install -e c:\path\to\package\ZS-Content-Checker\
    python -m pip install -e h:\github.com\Zoynels\nbopen_windows\

Usage::

    nbopen_windows AwesomeNotebook.ipynb

If double click on notebooks not work, then, run:

* Windows: ``python -m nbopen_windows.install_win``

