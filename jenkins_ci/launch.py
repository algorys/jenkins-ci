#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Jenkins Launch launch the specified job
"""

import sys

from jenkins_ci.build import launch_job
from jenkins_ci.settings import *

# Actions
commands = {
    'help':
        'Display this helpful message',
    'build':
        'Build specified job on default branch or specified branch',
    'info':
        'Display Job informations, like parameters or url'
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
    print('    %sjenkins-ci {command} {job} <params>%s\n' % (OK, ENDC))
    print('- %s{command}%s: command to execute' % (WARN, ENDC))
    for command in commands:
        print('    - %s: %s' % (command, commands[command]))
    print('- %s{job}%s: job to trigger' % (WARN, ENDC))
    if available_jobs:
        for _job in available_jobs:
            print('    - %s' % _job)
    else:
        print('    No Jobs has been configured in settings.ini !')
    print('- %s<params>%s: parameters of specified job, separate by colon. (optional)' % (WARN, ENDC))
    print('    %sWARNING%s: Parameters must respect order of job !' % (PURPLE, ENDC))


def main():
    """
    Main function of Jenkins-CI

    """

    # Parse ARGs
    if len(sys.argv) > 1:
        if sys.argv[1] in commands:
            # Build
            if sys.argv[1] == 'build':
                job_arg = sys.argv[2]
                job = config.get('jobs', job_arg)

                if job in jobs_name:
                    print("Start %s, waiting from Jenkins..." % config.get('jobs', job_arg))
                    params = []
                    if len(sys.argv) > 3:
                        params = sys.argv[3].split(':')
                    launch_job(job, params)
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

