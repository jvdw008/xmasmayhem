# https://cx-freeze.readthedocs.io/en/latest/overview.html
import sys
from cx_Freeze import setup, Executable

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": [], "excludes": ["tkinter"], "include_files": ["data", "ReadMe.txt"]}

setup(
    name="Xmas Mayhem",
    version="1.0",
    description="Xmas Mayhem - Help Santa deliver those goodies!",
    executables=[Executable("main.py", base=base, copyright="Copyright (C) 2022 Blackjet")],
    options={"build_exe": build_exe_options},
)