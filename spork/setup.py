import os, cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="Spork",
    options={"build_exe": {"packages": ["pygame"],
                           "include_files": [os.getcwd() + "/data"]}},
    executables=executables
)
