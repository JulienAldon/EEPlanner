from setuptools import setup

setup(
    name='eeplanner',
    version='2.0.1',
    license='',
    author='Julien Aldon',
    author_email='julien.aldon@epitech.eu',
    description='Créer des événements pour une activitée donnée',
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
        'pygobject',
        'glib',
        'yawaei==0.0.7'
    ],
    extras_require={
        'dev': [
            'twine'
        ]
    },
    data_files=[
        ('lib/eeplanner', ['Application2.glade']),
        ('share/applications', ['application-eeplanner.desktop'])
    ],
    entry_points={
        'console_scripts': [
            'eeplanner = eeplanner.interface:start'
        ]
    }
)

