#!/bin/bash
# create a virtual python environment for this app
# prerequisite: apt-get install python-virtualenv
virtualenv env
# maybe upgrade pip
env/bin/pip install --upgrade pip
# set it up for development
env/bin/python setup.py develop
# initialize the database
env/bin/initialize_speedfunding_db development.ini
# start the app (reload restarts the app when code changes: agile!)
env/bin/pserve development.ini --reload
