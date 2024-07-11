from setuptools import setup

APP = ['main.py']  # Replace with your script name
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['rumps', 'pandas', 'datetime'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)