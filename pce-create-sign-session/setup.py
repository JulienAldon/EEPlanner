import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ['gi']}

setup(
    name="EventOtron",
    version="0.0.1-3000",
    description="La kalash à event",
    options={"build_exe": build_exe_options},
    executables=[Executable("interface.py", target_name="eventotron")],
)