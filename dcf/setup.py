#!/usr/bin/env python3

from setuptools import setup

dependencies = ['click', 'boto3', 'prettytable', 'termcolor',
                'pyyaml>=3.13,<4.0', 'pyopenssl', 'python-jenkins', 
                'click_shell', 'PyGithub', 'python-dateutil', 'requests',
                'cryptography>=2.8']

setup(
        name='dcf',
        version='0.0.1',
        description='The DevOps Control Framework CLI',
        url='https://github.com/bunnyshankar/Manage_Github_Jenkins',
        author='Shankar Busetty',
        author_email='bunny.shankar@gmail.com',
        install_requires=dependencies,
        packages=['cli'],
        entry_points={
            'console_scripts': [
                'devops=cli.dcf:dcf'
            ]
        }
)
