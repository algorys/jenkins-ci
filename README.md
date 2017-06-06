# Jenkins Tool

Allow to build the wanted job on a specific branch

## Requirements

You should have Python installed on your device. This script is compatible with Python 2.7 and Python 3+.

## Installation

Unix:

```bash
# clone repository and go inside.
cd jenkins-ci/
sudo pip install .
```

Windows

```bash
# clone repository and go inside.
cd jenkins-ci/
sudo pip install .
```

## Usage

Script have a `help` command to display usage:

```bash
jenkins-ci -h
```

Let's say we have the following data:

- Jenkins user: `admin`
- User token: `y1y1y1y1y1y1`
- One job called : `job1` with the parameters `gitlabSourceBranch` and `dependencies`.

We will run the following command:

```bash
jenkins-ci -u admin -p y1y1y1y1y1y1 -j job1 --data dev:ON
```

The script will run the job **job1** with parameters `gitlabSourceBranch:dev, dependencies:ON`. Obviously, the user **must have the rights to run the job**.
