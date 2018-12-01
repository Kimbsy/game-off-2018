import os, cx_Freeze

executables = [cx_Freeze.Executable("spork.py")]

cx_Freeze.setup(
    name="Spork",
    options={"build_exe": {"packages": ["pygame"],
                           "include_files": [
                               os.getcwd() + "/data",
                               "ARCADECLASSIC.TTF",
                           ]}},
    executables=executables
)
