#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup

__version__ = "1.0.3"


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


def getversion():
    if 'BUILD_VERSION' in os.environ:
        return os.environ['BUILD_VERSION']
    else:
        return __version__


setup(
    name='pytest-azurepipelines',
    version=getversion(),
    author='Anthony Shaw',
    author_email='anthonyshaw@apache.org',
    maintainer='Anthony Shaw',
    maintainer_email='anthonyshaw@apache.org',
    license='MIT',
    url='https://github.com/tonybaloney/pytest-azurepipelines',
    description='Formatting PyTest output for Azure Pipelines UI',
    long_description=read('README.rst'),
    py_modules=['pytest_azurepipelines'],
    python_requires='>=3.5',
    data_files=[('resources', ['resources/style.css'])],
    install_requires=['pytest>=5.0.0', 'pytest-nunit>=1.0.0'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'azurepipelines = pytest_azurepipelines',
        ],
    },
)
