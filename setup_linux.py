from cx_Freeze import setup, Executable

setup(name="GUI Test",
      description="GUITest",
      version="0.1",
      options={"build_exe": {"build_exe": "Bin/pygobject",
                             "create_shared_zip": False,
                             "packages": ["gi","_cffi_backend", 'os', 'requests', 'tkinter', 'bcrypt', 'csv',
                                          'yahoo_fin.stock_info', 'datetime', 'rpy2', 'numpy', 'matplotlib',
                                          'idna.idnadata', 'pandas', 'jinja2', 'asyncio'],
                             }},
      executables=[Executable(script="main.py",
                              targetName="ValorizadorDeOpciones",
                              appendScriptToExe=True,
                              )]
      )
