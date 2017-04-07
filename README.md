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

Script have a `help` command to display the following:

```bash
jenkins-ci {command} {job} <params>
- Commands:
    - build: Build specified job on default branch or specified branch
    - help: Display this helpful message
    - info: Display Job informations: like params or url
- Available Jobs:
    - core
    - graphs
    - datasec
    - sqlite
    - elec
    - gcs
    - security
    - graphics
    - document
```