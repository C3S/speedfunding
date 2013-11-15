#!/bin/bash

virtualenv env

env/bin/pip install --upgrade pip

env/bin/python setup.py develop

