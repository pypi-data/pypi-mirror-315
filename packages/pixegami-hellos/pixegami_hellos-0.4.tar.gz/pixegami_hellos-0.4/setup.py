from setuptools import setup, find_packages

setup(
    name='pixegami_hellos',
    version='0.4',
    packages=find_packages(),
    install_requires=[
        'Flask','Flask-SQLAlchemy'
    ],  # If you have dependencies, add them here
)
