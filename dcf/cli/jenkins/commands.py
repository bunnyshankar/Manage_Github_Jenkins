''' Jenkins Commands '''

import click
from click.exceptions import Exit

@click.group()
def jenkins():
    ''' Jenkins administration commands '''

@jenkins.command()
@click.option('--user', help='Jekins username to login', required=True)
@click.option('--token', help='Jekins api token for username', required=True)
@click.pass_obj
def list_jobs(ctx, user, token):
    ''' List Folders and  Jobnames '''
    from dcf.cli.jenkins import list_jenkins_jobs
    if not list_jenkins_jobs(ctx, user, token):
        raise Exit(1)

@jenkins.command()
@click.argument('branchname')
@click.option('--user', help='Jekins username to login', required=True)
@click.option('--token', help='Jekins api token for username', required=True)
@click.option(
    '--jobname',
    help='Jobname in which branch has to be added. JobName should include foldername as well',
    required=True
)
@click.pass_obj
def add_branch(ctx, user, token, jobname, branchname):
    ''' Add Branch to a MultiBranch Jenkins Pipeline '''
    from dcf.cli.jenkins import add_github_branch
    if not add_github_branch(ctx, user, token, jobname, branchname):
        raise Exit(1)

@jenkins.command()
@click.argument('branchname')
@click.option('--user', help='Jekins username to login', required=True)
@click.option('--token', help='Jekins api token for username', required=True)
@click.option(
    '--jobname',
    help='Jobname in which branch has to be deleted. JobName should include foldername as well',
    required=True
)
@click.pass_obj
def delete_branch(ctx, user, token, jobname, branchname):
    ''' Delete Branch from a MultiBranch Jenkins Pipeline '''
    from dcf.cli.jenkins import delete_github_branch
    if not delete_github_branch(ctx, user, token, jobname, branchname):
        raise Exit(1)

@jenkins.command()
@click.argument('reponame')
@click.option('--user', help='Jekins username to login', required=True)
@click.option('--token', help='Jekins api token for username', required=True)
@click.option('--foldername', help='Foldername in which this job has to be created.', required=True)
@click.option(
    '--script',
    help='Jenkinfile to use.',
    type=click.Choice([
        'Jenkinsfile',
        'Jenkinsfile.arm64',
        'Jenkinsfile.java',
        'Jenkinsfile.python'
    ], case_sensitive=False),
    default='Jenkinsfile'
)
@click.pass_obj
def create_job(ctx, user, token, foldername, reponame, script):
    ''' Creeate a  MultiBranch Jenkins Pipeline job '''
    from dcf.cli.jenkins import create_jenkins_job
    if not create_jenkins_job(ctx, user, token, foldername, reponame, script):
        raise Exit(1)

@jenkins.command()
@click.option('--user', help='Jekins username to login', required=True)
@click.option('--token', help='Jekins api token for username', required=True)
@click.option(
    '--jobname',
    help='Jobname to check. jobName should include foldername as well',
    required=True
)
@click.pass_obj
def check_job(ctx, user, token, jobname):
    ''' check if job exists or not '''
    from dcf.cli.jenkins import check_jenkins_job
    if not check_jenkins_job(ctx, user, token, jobname):
        raise Exit(1)

@jenkins.command()
@click.argument('branch')
@click.option('--user', help='Jekins username to login', required=True)
@click.option('--token', help='Jekins api token for username', required=True)
@click.option('--jobname', help='JobName should include foldername as well', required=True)
@click.pass_obj
def get_build_history(ctx, user, token, jobname, branch):
    ''' Get Build Numbers History for the Branch '''
    from dcf.cli.jenkins import get_build_history
    if not get_build_history(ctx, user, token, jobname, branch):
        raise Exit(1)

@jenkins.command()
@click.argument('branch')
@click.option('--user', help='Jekins username to login', required=True)
@click.option('--token', help='Jekins api token for username', required=True)
@click.option('--jobname', help='JobName should include foldername as well', required=True)
@click.option(
    '--buildnumber',
    help='BuildNumber for which you need console output',
    required=True,
    type=int
)
@click.pass_obj
def get_build_log(ctx, user, token, jobname, branch, buildnumber):
    ''' Get Build log output for a given build  in a Branch '''
    from dcf.cli.jenkins import get_build_console_log
    if not get_build_console_log(ctx, user, token, jobname, branch, buildnumber):
        raise Exit(1)
