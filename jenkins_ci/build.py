#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Build contains jenkins access
"""

import sys
import time
import pycurl
import json

from io import BytesIO
from jenkinsapi.jenkins import Jenkins
from jenkinsapi.utils.crumb_requester import CrumbRequester

from jenkins_ci.settings import *


def launch_job(jobname, params):
    """
    Launch the job "jobname" with specified param "branch"

    :param jobname: the name of the job
    :type jobname: str
    :param params: params of job
    :type params: list
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

    # Get Job
    job = jenkins_server.get_job(jobname)
    # Fill parameters
    _params = job.get_params()
    job_params = {}
    matrix = 0
    for param in _params:
        if params:
            job_params[param['name']] = params[matrix]
            matrix += 1
        else:
            job_params[param['name']] = param['defaultParameterValue']['value']
    # Trigger build
    jenkins_server.build_job(jobname, params=job_params)
    job_started(job)

    # Display result
    build = job.get_last_build()
    print('Build #%s %s with params %s' % (
        build.get_number(), color(build.get_status()), job_params)
    )
    print('    Commit: %s' % build.get_revision()[:7])
    print('    See on %s' % job.url)

    matrices = build.get_matrix_runs()
    if matrices:
        print('Details of the matrix:')
        for matrix in matrices:
            print('%s: %s' % (matrix.name, color(matrix.get_status())))

    header = BytesIO()
    body = BytesIO()

    curl = pycurl.Curl()
    curl.setopt(pycurl.USERNAME, jenkins_user)
    curl.setopt(pycurl.PASSWORD, api_token)
    curl.setopt(pycurl.URL, str(build.get_result_url()).replace('python', 'json'))
    curl.setopt(pycurl.HEADERFUNCTION, header.write)
    curl.setopt(pycurl.WRITEFUNCTION, body.write)
    curl.perform()

    tests_result = json.loads(body.getvalue().decode('UTF-8'))
    print('Unit Tests:')
    for tests in tests_result['childReports']:
        if tests['result']['failCount'] == 0:
            print('    All Tests Results %s: %s' % (tests['child']['url'], color('PASSED')))
        else:
            print('    One or more tests %s: %s' % (tests['child']['url'], color('FAILED')))
            for test in tests['result']['suites']:
                for case in test['cases']:
                    if 'PASSED' not in case['status']:
                        print('    -!- Test %s: %s' % (case['name'], color(case['status'])))


def color(status):
    """
    TODO
    :param status:
    :return:
    """

    if 'PASSED' in status or 'SUCCESS' in status:
        return '%s%s%s' % (OK, status, ENDC)
    else:
        return '%s%s%s' % (FAIL, status, ENDC)


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
    print('Job [%s] is %srunning%s...' % (job.name, OK, ENDC))
    check_job_progress(job)
