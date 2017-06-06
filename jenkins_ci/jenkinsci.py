#!/usr/bin/env python
# -*- coding:utf-8 -*-

import argparse
import sys
import time
import pycurl
import json
from io import BytesIO
from jenkinsapi.jenkins import Jenkins
from jenkinsapi.utils.crumb_requester import CrumbRequester

JENKINS_URL = 'http://jenkins.alpi-net.com'
# Common VAR
OK = '\033[92m'
BLUE = '\033[94m'
PURPLE = '\033[95m'
WARN = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'


def launch():
    """
    TODO
    :return:
    """

    data = {
        'user': '',
        'token': '',
        'job': '',
        'params': ''
    }

    parser = argparse.ArgumentParser(description='Launch a Jenkins job with its parameters')
    required_args = parser.add_argument_group('Required arguments')
    required_args.add_argument('-u', type=str, help='Jenkins user who can trigger the job')
    required_args.add_argument('-p', help='User\'s jenkins password or token')
    required_args.add_argument('-j', help='Jenkins job to launch, without its namespace')
    parser.add_argument(
        '--data',
        help='Job parameters separated by colons (Parameters should follow order of the Job)'
    )

    args = parser.parse_args()

    if args.u and args.p and args .j:
        data['user'] = args.u
        data['token'] = args.t
        data['job'] = args.j
    else:
        parser.print_help()
        sys.exit(0)

    if args.data:
        data['params'] = args.data

    launch_job(data)


def get_jenkins_instance(user, token):
    """
    TODO
    :param user:
    :param token:
    :return:
    """

    # Jenkins Server
    crumb_requester = CrumbRequester(
        baseurl=JENKINS_URL,
        username=user,
        password=token
    )

    jenkins_server = Jenkins(
        baseurl=JENKINS_URL,
        username=user,
        password=token,
        requester=crumb_requester
    )

    return jenkins_server


def launch_job(data):
    """
    Launch the job "jobname" with specified param "branch"

    :param data: params of job
    :type data: dict
    :return:
    """

    # Initialize client
    jenkins_server = get_jenkins_instance(data['user'], data['token'])

    # Get Job
    job = jenkins_server.get_job(data['job'])

    # Initialize parameters
    params = data['params'].split(':')
    server_params = job.get_params()
    job_params = {}
    matrix = 0
    for param in server_params:
        if params:
            job_params[param['name']] = params[matrix]
            matrix += 1
        else:
            job_params[param['name']] = param['defaultParameterValue']['value']

    # Trigger build
    jenkins_server.build_job(data['job'], params=job_params)
    check_job_progress(job, job_params)

    display_job_result(job, data)


def check_job_progress(job, job_params):
    """
    TODO
    :param job:
    :param job_params:
    :return:
    """

    # Check Job start
    while not job.is_running():
        for i in range(15):
            sys.stdout.write("   ")
            x = i % 4
            sys.stdout.write('\r' + "." * x)
            time.sleep(0.5)
            sys.stdout.flush()
    print('Job [%s] is %srunning%s...' % (job.name, OK, ENDC))
    print('...with params: %s' % job_params)

    # Check Job is finished
    while job.is_running():
        for i in range(15):
            sys.stdout.write("   ")
            x = i % 4
            sys.stdout.write('\r' + "." * x)
            time.sleep(0.5)
            sys.stdout.flush()
    print('%s has finished' % job.name)


def display_job_result(job, data):
    """
    TODO
    :param job:
    :param data:
    :return:
    """

    # Display result
    build = job.get_last_build()
    print('Build #%s : %s' % (
        build.get_number(), color(build.get_status()))
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
    curl.setopt(pycurl.USERNAME, data['user'])
    curl.setopt(pycurl.PASSWORD, data['token'])
    curl.setopt(pycurl.URL, str(build.get_result_url()).replace('python', 'json'))
    curl.setopt(pycurl.HEADERFUNCTION, header.write)
    curl.setopt(pycurl.WRITEFUNCTION, body.write)
    curl.perform()

    tests_result = json.loads(body.getvalue().decode('UTF-8'))
    print('Unit Tests:')
    for tests in tests_result['childReports']:
        if tests['result']['failCount'] == 0:
            print('    All Tests Results %s: %s' % (color('PASSED'), tests['child']['url'], ))
        else:
            print('    One or more tests %s: %s' % (color('FAILED'), tests['child']['url']))
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


if __name__ == "__main__":
    launch()
