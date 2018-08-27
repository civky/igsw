from cx_Freeze import setup, Executable
import os
import sys

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = r'C:\Program Files\Python36\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Program Files\Python36\tcl\tk8.6'
productName = "ValorizadorDeOpciones"
build_exe_options = {"packages": ["_cffi_backend", 'os', 'requests', 'tkinter', 'bcrypt', 'csv', 'yahoo_fin.stock_info',
                                  'datetime', 'rpy2', 'numpy', 'matplotlib', 'idna.idnadata', 'pandas', 'jinja2',
                                  'asyncio'],
                     'include_files': [
                           os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
                           os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
                     ]}

exe = Executable(
      script="main.py",
      base="Win32GUI",
      targetName="ValorizadorDeOpciones.exe"
     )
setup(
      name="ValorizadorDeOpciones.exe",
      version="1.0",
      author="SteelWolf",
      description="Copyright 2018",
      options={"build_exe": build_exe_options},
      executables=[exe]
      )
