Open notebooks from the command line

nbopen looks for the nearest running notebook server - if it finds one, it
opens a web browser to that notebook. If not, it starts a new notebook server
in that directory.

Installation::

    python3 -m pip install nbopen_windows

Usage::

    nbopen AwesomeNotebook.ipynb

To integrate with your file manager, so you can double click on notebooks
to open them, run:

* Windows: ``python3 -m nbopen.install_win``

