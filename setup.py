#!/usr/bin/env python

from setuptools import setup
setup(name='shotgun',
	version='3.0',
	description='Shotgun python api, taken from github',
	author='Andrew Bunday',
	author_email='andrew.bunday@baseblack.com',
	maintainer_email='requests@baseblack.com',
	#py_modules=['shotgun.api.shotgun_api3'],
	packages=['shotgun','shotgun.api']
	)