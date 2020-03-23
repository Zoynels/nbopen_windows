import io
import os
import re
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from notebook.utils import check_pid
from jupyter_core.paths import jupyter_runtime_dir, jupyter_path

try:
  import winreg
except ImportError:  
  import _winreg as winreg


# Not fully clear files in standart function
# TODO: After change in standart function -- delete this function
def list_running_servers_v2(runtime_dir=None):
    """Iterate over the server info files of running notebook servers.
    
    Given a runtime directory, find nbserver-* files in the security directory,
    and yield dicts of their information, each one pertaining to
    a currently running notebook server instance.
    """

    if runtime_dir is None:
        runtime_dir = jupyter_runtime_dir()

    # The runtime dir might not exist
    if not os.path.isdir(runtime_dir):
        return

    for file_name in os.listdir(runtime_dir):
        if re.match('nbserver-(.+).json', file_name):
            with io.open(os.path.join(runtime_dir, file_name), encoding='utf-8') as f:
                info = json.load(f)

            # Simple check whether that process is really still running
            # Also remove leftover files from IPython 2.x without a pid field
            if ('pid' in info) and check_pid(info['pid']):
                #yield info
                pass
            else:
                # If the process has died, try to delete its info file
                try:
                    os.unlink(os.path.join(runtime_dir, file_name))
                except OSError:
                    pass  # TODO: This should warn or log or something

                try:
                    os.unlink(os.path.join(runtime_dir, file_name)[:-5] + "-open.html")
                except OSError:
                    pass  # TODO: This should warn or log or something

        # Delete all "*-open.html" files which hasn't pair json
        if re.match('nbserver-(.+)-open.html', file_name):
            if os.path.isfile(os.path.join(runtime_dir, file_name)[:-10] + ".json"):
                pass
            else:
                try:
                    os.unlink(os.path.join(runtime_dir, file_name))
                except OSError:
                    pass  # TODO: This should warn or log or something

def is_downloadebal_url(url, timeout=0.1):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    try:
        response = requests.get(url, stream=False, verify=False, timeout=timeout)
        if response.status_code == 200:
            return True
        else:
            raise ValueError(f"response: {response.status_code}")
    except:
        return False

def read_opt_timout():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Classes\Jupyter.nbopen_windows\shell\open\command", 0, winreg.KEY_READ)
    for i in range(0, winreg.QueryInfoKey(key)[1]):
        v = winreg.EnumValue(key, i)
        if v[0].lower() == "timeout":
            return float(v[1])
    return 1
