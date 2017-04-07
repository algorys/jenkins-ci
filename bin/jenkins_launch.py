#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Jenkins Launch launch the specified job
"""

import os
import subprocess
import sys

from jenkins_ci.build import launch_job
from jenkins_ci.settings import config


def usage(jobs):
    """
    TODO
    :return:
    """

    print("Usage: %s [command] [job]" % os.path.basename(__file__))
    print("- Available jobs:")
    for _job in jobs:
        print('    - %s' % _job)


if __name__ == '__main__':
    # VARIABLES
    branch_output = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
    branch = branch_output.decode('UTF-8').split('\n')[0]
    jobs_name = []
    available_jobs = []
    for key, value in config.items('jobs'):
        jobs_name.append(value)
        available_jobs.append(key)

    if len(sys.argv) > 1:
        job_arg = sys.argv[1]

        job = config.get('jobs', job_arg)

        if job in jobs_name:
            print("Compile %s" % config.get('jobs', job_arg))

            launch_job(job, branch)
        else:
            print('ERROR: job %s not found in  ' % job_arg)
            usage(available_jobs)
    else:
        usage(available_jobs)
