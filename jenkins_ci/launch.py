#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Jenkins Launch launch the specified job
"""

import subprocess
import sys

from jenkins_ci.build import launch_job
from jenkins_ci.settings import config

# Actions
commands = {
    'help':
        'Display this helpful message',
    'build':
        'Build specified job on default branch or specified branch',
    'info':
        'Display Job informations: like params or url'
}

# Jobs
jobs_name = []
available_jobs = []
for key, value in config.items('jobs'):
    jobs_name.append(value)
    available_jobs.append(key)


def usage():
    """
    Display usage message

    """

    print('Usage:')
    print('    jenkins-ci build {job} {params}')
    print('    jenkins-ci info {job}')
    print('- Commands:')
    for command in commands:
        print('    - %s: %s' % (command, commands[command]))
    print('- Available Jobs:')
    if available_jobs:
        for _job in available_jobs:
            print('    - %s' % _job)
    else:
        print('    No Jobs has been configured in settings.ini !')
    print('- Params: parameters of specified job, separate by colon.')


def main():
    """
    Main function of Jenkins-CI

    """

    # Branch
    branch_output = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
    branch = branch_output.decode('UTF-8').split('\n')[0]

    # Parse ARGs
    if len(sys.argv) > 1:
        if sys.argv[1] in commands:
            # Build
            if sys.argv[1] == 'build':
                job_arg = sys.argv[2]
                job = config.get('jobs', job_arg)

                if job in jobs_name:
                    print("Build %s" % config.get('jobs', job_arg))
                    launch_job(job, branch)
                else:
                    print('ERROR: job %s not found...' % job_arg)
                    usage()
            # Info
            elif sys.argv[1] == 'info':
                print('NOT IMPLEMENTED !')
            else:
                usage()
        else:
            print('This action is not valid !')
            usage()
    else:
        usage()

if __name__ == '__main__':
    main()

