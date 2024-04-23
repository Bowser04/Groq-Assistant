import subprocess
import os
import platform
print(platform.python_version())
print("Create venv ...")
os.system("python --version")
os.system("python -m venv venv")
# Path to a Python interpreter that runs any Python script
# under the virtualenv /path/to/virtualenv/
pip_bin = "venv\Scripts\pip.exe"
python_bin = "venv\Scripts\python.exe"
os.system(python_bin+" --version")
# Path to the script that must run under the virtualenv
script_file = " install -r requirement.txt"
print("install requirement ...")
os.system(pip_bin+script_file)
os.system(python_bin+" hash_key.py")
os.system(python_bin+" install.py")