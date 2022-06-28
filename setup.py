import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os", "random", "tkinter", "PIL", "requests", "json"],
}

# GUI applications require a different base on Windows (the default is for
# a console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="ShipProject",
    version="0.2",
    description="smth",
    options={"build_exe": build_exe_options},
    executables=[Executable("app.py", base=base)],
)
