#!/usr/bin/env python
"""Python setup script for the wordseg package

This script is not intented to be use directly but must be configured
by cmake.

"""

import os
from setuptools import setup


long_description = '''
Please see the online documentation at https://wordseg.readthedocs.io

The wordseg package provides **a collection of tools for text based
word segmentation** covering both text preprocessing, segmentation
algorithms, evaluation and statistics relevant for word segmentation
studies. It can be used from **bash** and **python**.'''


def on_readthedocs():
    """Return True if building the online documentation on readthedocs"""
    return os.environ.get('READTHEDOCS', None) == 'True'


def bin_targets():
    """Return the list of binaries to be installed with wordseg"""
    if on_readthedocs():
        return []
    else:
        return [os.path.join(
            '/home/travis/build/bootphon/wordseg/build', 'wordseg', 'algos', algo, algo)
                for algo in ('ag', 'dpseg')]


def data_files(binary):
    """Return a list of exemple configuration files bundled with `binary`"""
    data_dir = os.path.join(
        '/home/travis/build/bootphon/wordseg', 'data', binary)
    return [os.path.join(data_dir, f) for f in os.listdir(data_dir)]


setup(
    name='wordseg',
    version='0.5.1',
    description='tools for text based word segmentation',
    long_description=long_description,
    author='Alex Cristia, Mathieu Bernard, Elin Larsen',
    url='https://github.com/bootphon/wordseg',
    license='GPL3',
    zip_safe=True,

    package_dir={
        'wordseg': '/home/travis/build/bootphon/wordseg/wordseg',
        'wordseg.algos': '/home/travis/build/bootphon/wordseg/wordseg/algos'},
    packages=['wordseg', 'wordseg.algos'],

    install_requires=(['six', 'joblib'] if on_readthedocs() else
                      ['six', 'joblib', 'numpy', 'pandas']),
    tests_require=['pytest'],

    entry_points={'console_scripts': [
        'wordseg-prep = wordseg.prepare:main',
        'wordseg-eval = wordseg.evaluate:main',
        'wordseg-stats = wordseg.statistics:main',
        'wordseg-syll = wordseg.syllabification:main',
        'wordseg-baseline = wordseg.algos.baseline:main',
        'wordseg-ag = wordseg.algos.ag:main',
        'wordseg-dibs = wordseg.algos.dibs:main',
        'wordseg-dpseg = wordseg.algos.dpseg:main',
        'wordseg-tp = wordseg.algos.tp:main',
        'wordseg-puddle = wordseg.algos.puddle:main']},

    data_files=[
        ('bin', bin_targets()),
        ('data/syllabification', data_files('syllabification')),
        ('data/ag', data_files('ag')),
        ('data/dpseg', data_files('dpseg'))])
