import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ['gi']}

setup(
    name="EpitechEventPlanner",
    version="0.1.1",
    description="Créer des event sur une activitée donnée",
    options={"build_exe": build_exe_options},
    executables=[Executable("src/interface.py", target_name="EpitechEventPlanner")],
)