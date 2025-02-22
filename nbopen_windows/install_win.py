"""Install GUI integration on Windows"""

import sys

try:
  import winreg
except ImportError:  
  import _winreg as winreg

SZ = winreg.REG_SZ
with winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\Classes\.ipynb") as k:
    winreg.SetValue(k, "", SZ, "Jupyter.nbopen_windows")
    winreg.SetValueEx(k, "Content Type", 0, SZ, "application/x-ipynb+json")
    winreg.SetValueEx(k, "PerceivedType", 0, SZ, "document")
    with winreg.CreateKey(k, "OpenWithProgIds") as openwith:
        winreg.SetValueEx(openwith, "Jupyter.nbopen_windows", 0, winreg.REG_NONE, b'')

executable = sys.executable

# Default behavior
show_window = True
if show_window:
    if executable.lower().endswith("pythonw.exe"):
        executable = executable[:-len('pythonw.exe')] + 'python.exe'
else:
    if executable.lower().endswith("python.exe"):
        executable = executable[:-len('python.exe')] + 'pythonw.exe'

launch_cmd = '"{}" -m nbopen_windows "%1"'.format(executable)

with winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\Classes\Jupyter.nbopen_windows") as k:
    winreg.SetValue(k, "", SZ, "IPython notebook")
    with winreg.CreateKey(k, "shell\open\command") as launchk:
        winreg.SetValue(launchk, "", SZ, launch_cmd)
        winreg.SetValueEx(launchk, "timeout", 0, winreg.REG_SZ, "0.1")

try:
    from win32com.shell import shell, shellcon
    shell.SHChangeNotify(shellcon.SHCNE_ASSOCCHANGED, shellcon.SHCNF_IDLIST, None, None)
except ImportError:
    print("You may need to restart for association with .ipynb files to work")
    print("  (pywin32 is needed to notify Windows of the change)")
