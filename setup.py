from setuptools import setup
import sys

setup(
    name='eeplanner',
    version='2.0.1',
    license='',
    author='Julien Aldon',
    author_email='julien.aldon@epitech.eu',
    description='Créer des event pour une activitée donnée',
    url='https://github.com/JulienAldon/EEPlanner',
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
        'Yawaei==0.0.6'
    ],
    extras_require={
        'dev': [
            'twine'
        ]
    },
    data_files=[
        (f'{sys.prefix}/local/lib/eeplanner', ['Application2.glade']),
        (f'{sys.prefix}/local/share/applications', ['application-eeplanner.desktop'])
    ],
    entry_points={
        'console_scripts': [
            'eeplanner = eeplanner.interface:start'
        ]
    }
)

