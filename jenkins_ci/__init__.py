#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Jenkins CI is a jenkins tool to launch jenkins jobs
"""

# Application version and manifest
VERSION = (0, 1, 0)
__application__ = u"Jenkins-CI"
__pkg_name__ = u"jenkins-ci"
__short_version__ = '.'.join((str(each) for each in VERSION[:2]))
__version__ = '.'.join((str(each) for each in VERSION[:4]))
__author__ = u"Estrada Matthieu"
__author_email__ = u"m.estrada@alpi.fr"
__copyright__ = u"2016-2017 - %s" % __author__
__license__ = u"GNU Affero General Public License, version 3"
__description__ = u"Jenkins Tool to trigger Jenkins jobs"
__releasenotes__ = u"Jenkins Tool to trigger Jenkins jobs"
__project_url__ = "http://gitlab.alpi-net.com/mea/jenkins-ci"
__doc_url__ = "http://gitlab.alpi-net.com/mea/jenkins-ci"

# Application Classifiers
__classifiers__ = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Natural Language :: English',
    'Programming Language :: Python',
    'Topic :: Software Development :: Build Tools',
    'Topic :: Software Development :: Compilers'
]

# Application Manifest
manifest = {
    'name': __application__,
    'version': __version__,
    'author': __author__,
    'description': __description__,
    'copyright': __copyright__,
    'release': __releasenotes__,
    'url': __project_url__,
    'doc': __doc_url__
}