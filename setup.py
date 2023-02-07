import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "include_files": ["README.md"],
    "includes": ["AppKit"],
    "excludes": ["tkinter"],
}

setup(
    name = "menu",
    version = "0.1",
    options = {"build_exe": build_exe_options},
    executables = [Executable("SuperStudyMenu.py", base=None)] # change this line to set the base parameter
)
