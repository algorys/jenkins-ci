#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Build contains jenkins access
"""

import sys
import time

from jenkinsapi.jenkins import Jenkins
from jenkinsapi.utils.crumb_requester import CrumbRequester

from jenkins_ci.settings import config

# Common VAR
OK = '\033[92m'
WARN = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'


def launch_job(jobname, branch):
    """
    Launch the job "jobname" with specified param "branch"

    :param jobname: the name of the job
    :type jobname: str
    :param branch: wanted branch to compile
    :type branch: str
    :return:
    """

    # Jenkins VAR
    jenkins_url = config.get('jenkins', 'url')
    jenkins_user = config.get('jenkins', 'user')
    api_token = config.get('jenkins', 'api_token')

    # Jenkins Server
    crumb_requester = CrumbRequester(baseurl=jenkins_url, username=jenkins_user, password=api_token)
    jenkins_server = Jenkins(
        baseurl=jenkins_url, username=jenkins_user, password=api_token, requester=crumb_requester
    )

    # Start Build
    jenkins_server.build_job(jobname, params={'gitlabSourceBranch': branch})
    job = jenkins_server.get_job(jobname)

    job_started(job)

    build = job.get_last_build()

    if build.get_status == "SUCCESS":
        print('Build %s%s%s on %s' % (OK, build.get_status(), ENDC, branch))
    else:
        print('Build %s%s%s on %s' % (FAIL, build.get_status(), ENDC, branch))
    print(' Commit: %s' % build.get_revision()[:7])
    print(' See on %s' % job.url)
    print(build.get_result_url())
    print(build.get_resultset())
    print(build.get_artifact_dict())
    print(job.get_matrix_runs())


def check_job_progress(job):
    """
    TODO
    :return:
    """

    while job.is_running():
        for i in range(15):
            sys.stdout.write("   ")
            x = i % 4
            sys.stdout.write('\r' + "." * x)
            time.sleep(0.5)
            sys.stdout.flush()

    print('%s has finished' % job.name)


def job_started(job):
    """
    Check if job is stated or not

    :param job: job triggered
    :type job: jenkinsapi.job.Job
    """

    while not job.is_running():
        for i in range(15):
            sys.stdout.write("   ")
            x = i % 4
            sys.stdout.write('\r' + "." * x)
            time.sleep(0.5)
            sys.stdout.flush()
    print('Job [%s] is running...' % job.name)
    check_job_progress(job)
