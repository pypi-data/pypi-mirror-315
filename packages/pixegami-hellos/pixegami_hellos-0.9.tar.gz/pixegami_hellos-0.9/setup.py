# setup.py
from setuptools import setup, find_packages

setup(
    name='pixegami_hellos',
    version='0.9',
    packages=find_packages(),  # Automatically find all packages in the directory
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
    ],
)
