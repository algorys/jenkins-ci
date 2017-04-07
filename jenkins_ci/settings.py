#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Settings contains script configurations
"""

import os
import configparser
from configparser import DuplicateOptionError, DuplicateSectionError

# Common VAR
OK = '\033[92m'
BLUE = '\033[94m'
PURPLE = '\033[95m'
WARN = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'


def get_config_location():
    """
    TODO
    :return:
    """

    settings_filenames = [
        os.path.abspath('../etc/settings.ini'),
        '/usr/local/etc/jenkins-ci/settings.ini',
        '%s/.local/jenkins-ci/settings.ini' % os.environ['HOME']
    ]

    return settings_filenames


def init_config():
    """

    :return:
    """

    _config = configparser.ConfigParser()

    try:
        _config.read(get_config_location())
    except (DuplicateOptionError, DuplicateSectionError) as e:
        print(e)
    except Exception as f:
        print(f)

    return _config

config = init_config()
