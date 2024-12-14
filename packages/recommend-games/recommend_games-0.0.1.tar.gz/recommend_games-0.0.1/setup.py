from setuptools import setup, find_packages
setup(
name='recommend_games',
version='0.0.1',
author='Andrew Rawson',
email='arawson@proton.me',
description='A simple Python package that simulates a recommendation engine',
packages=find_packages(),
classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
],
python_requires='>= 3.12'
)

