#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup, find_packages
except:
    sys.exit("Error: missing python-setuptools library")

try:
    python_version = sys.version_info
except:
    python_version = (1, 5)

if python_version < (2, 7):
    sys.exit("This application requires a minimum Python 2.7.x, sorry!")

# Create manifest
with open(os.path.join('jenkins_ci/__init__.py')) as fh:
    manifest = {}
    exec(fh.read(), manifest)

package_name = manifest["__pkg_name__"]

data_files = [
    ('etc/jenkins-ci', ['etc/settings.ini']),
    # ('bin', ['bin/jenkins_ci']),
]

setup(
    # Package name and version
    name=manifest["__pkg_name__"],
    version=manifest["__version__"],

    # Metadata for PyPI
    author=manifest["__author__"],
    author_email=manifest["__author_email__"],
    keywords="jenkins ci",
    url=manifest["__project_url__"],
    license=manifest["__license__"],
    description=manifest["__description__"],
    long_description=open('README.md').read(),

    classifiers=manifest["__classifiers__"],

    # Unzip Egg
    zip_safe=False,

    # Package data
    packages=find_packages(),
    include_package_data=True,

    # Where to install distributed files
    data_files=data_files,

    # Dependencies (if some) ...
    install_requires=[
        'jenkinsapi'
    ],

    # Entry points (if some) ...
    entry_points={
        'console_scripts': [
            'jenkins-ci = jenkins_ci.launch:main'
        ],
    }
)
