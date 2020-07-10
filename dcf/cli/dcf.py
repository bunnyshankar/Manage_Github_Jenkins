#!/usr/bin/env python3

''' DevOps Control Framework CLI '''

import os
import sys
import logging
from logging.config import dictConfig
import queue
import click
from click_shell import shell
from click.exceptions import Exit
from dcf.misc.misc import read_yaml, write_yaml

from .jenkins import commands as jenkins
from .github import commands as github

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class Config(object):
    ''' Top level context object '''
    def __init__(self, profile, dcf_profile, region, shell,
                 quiet=False, debug=False):
        self.config_dir = os.path.join(os.getenv('HOME'), '.dcf')
        self.home = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), '..'
        )
        self.shell = shell
        self.quiet = quiet
        self.debug = debug
        self.region = region
        self.profile = None
        self.dcf_profile = None
        if dcf_profile:
            if not self.load_profile(dcf_profile):
                raise Exit(1)
        if profile:
            self.profile = profile
        logging_config = read_yaml(
            os.path.join(self.home, 'config', 'cli_logging.yaml')
        )
        log_dir = os.path.join(os.getenv('HOME'), '.dcf', 'logs')
        if not os.path.isdir(log_dir):
            os.makedirs(log_dir)
        logging_config['handlers']['file']['filename'] = os.path.join(
            log_dir,
            logging_config['handlers']['file']['filename'])
        dictConfig(logging_config)
        self.console_logger = logging.getLogger('console')
        self.file_logger = logging.getLogger()
        self.logger = self.console_logger
        if debug:
            self.console_logger.setLevel(logging.DEBUG)
        else:
            self.console_logger.setLevel(logging.INFO)
        self.cli = True

    def load_profile(self, profile):
        ''' Load profile from config file '''
        profile_file = os.path.join(self.config_dir, 'dcf_profiles')
        if os.path.exists(profile_file):
            dcf_config = read_yaml(profile_file)
            if profile in dcf_config:
                self.dcf_profile = profile
                cfg = dcf_config[profile]
                if 'profile' in cfg:
                    self.profile = cfg['profile']
                if 'region' in cfg:
                    self.region = cfg['region']
                return True
        click.echo('Profile {} does not exist'.format(profile))
        return False

    def save_profile(self, profile):
        ''' Save current profile to config file '''
        profile_file = os.path.join(self.config_dir, 'dcf_profiles')
        if os.path.exists(profile_file):
            dcf_config = read_yaml(profile_file)
        else:
            dcf_config = {}

        dcf_config[profile] = {
            'backend': self.backend,
            'tenant': self.tenant
        }
        if self.profile:
            dcf_config[profile]['profile'] = self.profile
        if self.region:
            dcf_config[profile]['region'] = self.region
        write_yaml(profile_file, dcf_config)
        self.dcf_profile = profile
        click.echo('Saved profile {}'.format(profile))

    def delete_profile(self, profile):
        ''' Delete profile from config file '''
        profile_file = os.path.join(self.config_dir, 'dcf_profiles')
        if os.path.exists(profile_file):
            dcf_config = read_yaml(profile_file)
            if profile in dcf_config:
                del dcf_config[profile]
                write_yaml(profile_file, dcf_config)
                click.echo('Profile {} deleted'.format(profile))
                return
        click.echo('Profile {} does not exist'.format(profile))

    def list_profiles(self):
        ''' List available profiles '''
        profile_file = os.path.join(self.config_dir, 'dcf_profiles')
        if os.path.exists(profile_file):
            dcf_config = read_yaml(profile_file)
            if not dcf_config:
                click.echo('No profiles are stored')
                return
            for profile in dcf_config:
                click.echo(profile)
        else:
            click.echo('No profiles are stored')

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@shell(prompt='DevOps> ', intro='Starting DevOps Control Framework Shell...',
       hist_file=os.path.join(os.getenv('HOME'), '.dcf-history'),
       context_settings=CONTEXT_SETTINGS)
@click.option(
    '--aws-profile',
    envvar='AWS_PROFILE',
    help='AWS CLI profile to use if not default')
@click.option(
    '--profile',
    envvar='DCF_PROFILE',
    help='DCF profile to load')
@click.option(
    '--region',
    envvar='AWS_REGION',
    help='Override profile region')
@click.option('--quiet', is_flag=True, default=False,
              envvar='QUIET',
              help='Only output summary of actions')
@click.option('--debug/--no-debug', default=False,
              envvar='DEBUG',
              help='Debug output')
@click.pass_context
def dcf(ctx, aws_profile, profile, region, quiet, debug):
    ''' CLI '''
    shell = ctx.command.shell if not ctx.invoked_subcommand else None
    ctx.obj = Config(aws_profile, profile, region, shell, quiet, debug)

dcf.add_command(jenkins.jenkins)
dcf.add_command(github.github)
