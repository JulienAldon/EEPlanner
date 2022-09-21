# import sys
# from cx_Freeze import setup, Executable

# build_exe_options = {"packages": ['gi']}

# setup(
#     name="EpitechEventPlanner",
#     version="2.0.1",
#     description="Créer des event sur une activitée donnée",
#     options={"build_exe": build_exe_options},
#     executables=[Executable("src/interface.py", target_name="EpitechEventPlanner")],
# )

from setuptools import setup

setup(
    name='eeplanner',
    version='2.0.1',
    license='',
    author='Julien Aldon',
    author_email='julien.aldon@epitech.eu',
    description='Créer des event sur une activitée donnée',
    url='https://github.com/JulienAldon/EpitechEventPlanner',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Environment :: X11 Applications :: GTK',
    ],
    python_requires='>3.9',
    packages=[
        'eeplanner'
    ],
    include_package_data=True,
    install_requires=[
        'requests',
        'pycairo',
        'pygobject',
        'glib',
        'Yawaei'
    ],
    extras_require={
        'dev': [
            'twine'
        ]
    },
    data_files=[
        ('share/eeplanner', ['Application2.glade'])
    ],
    entry_points={
        'console_scripts': [
            'eeplanner = eeplanner.interface:start'
        ]
    }
)