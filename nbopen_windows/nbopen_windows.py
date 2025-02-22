#!/usr/bin/python3

import argparse
import os
import webbrowser

from jupyter_server.serverapp import ServerApp as notebookapp
from jupyter_server.serverapp import list_running_servers
from jupyter_server.utils import url_path_join, url_escape
import nbformat
from traitlets.config import Config
from .util import list_running_servers_v2, is_downloadebal_url, read_opt_timout


def find_best_server(filename):
    servers = []
    list_running_servers_v2() # TODO: After change in standart function -- delete this function
    for si in list_running_servers():
        if filename.lower().startswith(si['root_dir'].lower()):
            servers.append(si)
    try:
        return max(servers, key=lambda si: len(si['root_dir']))
    except ValueError:
        return None

def nbopen(filename):
    filename = os.path.abspath(filename)
    home_dir = os.path.expanduser('~')
    server_inf = find_best_server(filename)
    if (server_inf is not None) and \
        (is_downloadebal_url(server_inf["url"], timeout=read_opt_timout())):
        print("Using existing server at", server_inf['root_dir'])
        path = os.path.relpath(filename, start=server_inf['root_dir'])
        if os.sep != '/':
            path = path.replace(os.sep, '/')
        url = url_path_join(server_inf['url'], 'notebooks', url_escape(path))
        na = notebookapp()
        na.load_config_file()
        browser = webbrowser.get(na.browser or None)
        browser.open(url, new=2)
    else:
        if filename.lower().startswith(home_dir):
            nbdir = home_dir
        else:
            nbdir = os.path.dirname(filename)

        print("Starting new server")
        # Hack: we want to override these settings if they're in the config file.
        # The application class allows 'command line' config to override config
        # loaded afterwards from the config file. So by specifying config, we
        # can use this mechanism.
        cfg = Config()
        cfg.ServerApp.file_to_run = os.path.abspath(filename)
        cfg.ServerApp.root_dir = nbdir
        cfg.ServerApp.open_browser = True
        notebookapp.launch_instance(config=cfg,
                                        argv=[],  # Avoid it seeing our own argv
                                        )

def nbnew(filename):
    if not filename.lower().endswith('.ipynb'):
        filename += '.ipynb'
    if os.path.exists(filename):
        msg = "Notebook {} already exists"
        print(msg.format(filename))
        print("Opening existing notebook")
    else:
        nb_version = nbformat.versions[nbformat.current_nbformat]
        nbformat.write(nb_version.new_notebook(),
                       filename)
    return filename

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('-n', '--new', action='store_true', default=False,
                    help='Create a new notebook file with the given name.')
    ap.add_argument('filename', help='The notebook file to open')

    args = ap.parse_args(argv)
    if args.new:
        filename = nbnew(args.filename)
    else:
        filename = args.filename

    nbopen(filename)

if __name__ == '__main__':
    main()
