"""
the setup.py file describes your broject and the files that belong to it.
"""
from setuptools import find_packages, setup

setup(
    name='flaskr', # the name of the application
    version='1.0.0',
    # packages tells python what package dirtories(and the python files they contain) to include.
    # find_packages() find the diretories find the directories automatically.
    packages=find_packages(), 
    # to include other files, like static, templates.
    # python needs another file named MANIFEST.in to tell what other data is .
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)