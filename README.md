# Jenkins-CI

[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](http://www.repostatus.org/badges/latest/wip.svg)](http://www.repostatus.org/#wip)

Jenkins-CI allow you to build a jenkins job with its parameters, from any platform. This tool provides similar features to [Jenkins-CLI](https://jenkins.io/doc/book/managing/cli/) but it is in Python.

## Features

- display progression of Job directly in your console
- display if your Job SUCCESS, ABORTED or FAILED
- display link to tests results if job has Unit Tests
- and more...

## Requirements

You should have Python installed on your device. This script is normally compatible with Python 2.7 and Python 3+.

## Installation

Simply download this repository and type the following commands:

```bash
# clone repository and go inside.
cd jenkins-ci/

# Install Jenkins-CI
sudo pip install .
```

That's all !

## Usage

Script have a `help` command to display usage:

```bash
user@jenkins:~$ jenkins-ci -h
usage: jenkinsci.py [-h] [-u U] [-p P] [-j J] [--data DATA]

Launch a Jenkins job with its parameters

optional arguments:
  -h, --help   show this help message and exit
  --data DATA  Job parameters separated by colons (Parameters should follow
               order of the Job)

Required arguments:
  -u U         Jenkins user who can trigger the job
  -p P         User's jenkins password or token
  -j J         Jenkins job to launch, without its namespace
```

## Work with a config file

**Coming soon**

## Example

Let's say we have the following data:

- Jenkins user: `admin`
- User token: `y1y1y1y1y1y1`
- One job called : `job1` with the parameters `gitlabSourceBranch` and `dependencies`.

Obviously, the user **must have the rights to run the job** ! Then, simply run the following command:

```bash
jenkins-ci -u admin -p y1y1y1y1y1y1 -j job1 --data dev:ON
```

The script will:

* run the job **job1**
* with parameters `gitlabSourceBranch:dev, dependencies:ON`.

**Output example for a matrix job:**

```bash
user@jenkins:~$ jenkins-ci -u admin -p password -j My_Job --data dev
..Job [My_Job] is running...
...with params: {'gitlabSourceBranch': 'dev'}
..My_Job has finished
Build #411 : SUCCESS
    Commit: 891c682
    See on http://my-jenkins.com/job/MyGroup/job/My_Job
Details of the matrix:
MyGroup » My_Job » Debug,clang #411: SUCCESS
MyGroup » My_Job » Debug,gcc #411: SUCCESS
MyGroup » My_Job » Debug,vc2015 #411: SUCCESS
MyGroup » My_Job » Release,clang #411: SUCCESS
MyGroup » My_Job » Release,gcc #411: SUCCESS
MyGroup » My_Job » Release,vc2015 #411: SUCCESS
Unit Tests:
    All Tests Results PASSED: http://my-jenkins.com/job/MyGroup/job/My_Job/BUILD_TYPE=Release,compiler=vc2015/411/
    All Tests Results PASSED: http://my-jenkins.com/job/MyGroup/job/My_Job/BUILD_TYPE=Debug,compiler=gcc/411/
    All Tests Results PASSED: http://my-jenkins.com/job/MyGroup/job/My_Job/BUILD_TYPE=Debug,compiler=vc2015/411/
    All Tests Results PASSED: http://my-jenkins.com/job/MyGroup/job/My_Job/BUILD_TYPE=Release,compiler=clang/411/
    All Tests Results PASSED: http://my-jenkins.com/job/MyGroup/job/My_Job/BUILD_TYPE=Release,compiler=gcc/411/
    All Tests Results PASSED: http://my-jenkins.com/job/MyGroup/job/My_Job/BUILD_TYPE=Debug,compiler=clang/411/
