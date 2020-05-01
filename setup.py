#!/usr/bin/env python

import setuptools

def readme():
    with open('README.rst') as f:
        return f.read()

setuptools.setup(
    name             = 'cafplot',
    version          = '0.1',
    author           = 'Dmitrii Torbunov',
    author_email     = 'torbu001@umn.edu',
    classifiers      = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
    ],
    description      = 'Library to plot CAFAna objects in python/matplotlib',
    install_requires = [
        'numpy',
        'matplotlib',
        'scipy',
    ],
    license          = 'MIT',
    long_description = readme(),
    packages         = setuptools.find_packages(),
    url              = 'https://github.com/usert5432/cafplot',
)

