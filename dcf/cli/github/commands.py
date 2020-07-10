''' Github Commands '''

import click
from click.exceptions import Exit

@click.group()
def github():
    ''' Github administration commands '''

@github.command()
@click.option('--token', help='Github api token for username', required=True)
@click.pass_obj
def list_repos(ctx, token):
    ''' List Repositories in this account '''
    from dcf.cli.github import list_github_repos
    if not list_github_repos(ctx, token):
        raise Exit(1)

@github.command()
@click.argument('collabname')
@click.option('--token', help='Github api token for username', required=True)
@click.pass_obj
def list_repos_for_collab(ctx, collabname, token):
    ''' List repositories for a Collaborator '''
    from dcf.cli.github import list_collab_repos
    if not list_collab_repos(ctx, collabname, token):
        raise Exit(1)

@github.command()
@click.option('--user-grp', required=0, type=click.File(),
              help='File path to group of users. One user per line.')
@click.option('--user', required=0, type=click.STRING,
              help='Individual user you want to process')
@click.option('--repo-grp', required=1, type=click.File(),
              help='File with list of repositories (in user/repo format) to grant access to.')
@click.option('--token', help='Github api token for username', required=True)
@click.pass_obj
def grant_access(ctx, user_grp, repo_grp, user, token):
    ''' Grant access to repositor{ies) for user{s} '''
    from dcf.cli.github import github_repo_access
    if not user and not user_grp:
        raise click.UsageError('You must specify either --user or --user_grp or both.')
    if not github_repo_access(ctx, user_grp, repo_grp, user, token):
        raise Exit(1)

@github.command()
@click.option('--user-grp', required=0, type=click.File(),
              help='File path to group of users. One user per line.')
@click.option('--user', required=0, type=click.STRING,
              help='Individual user you want to process')
@click.option('--repo-grp', required=1, type=click.File(),
              help='File with list of repositories (in user/repo format) to reovke access to.')
@click.option('--token', help='Github api token for username', required=True)
@click.pass_obj
def revoke_access(ctx, user_grp, repo_grp, user, token):
    ''' Revoke access to repositor{ies) for user{s} '''
    from dcf.cli.github import github_revoke_access
    if not user and not user_grp:
        raise click.UsageError('You must specify either --user or --user_grp or both.')
    if not github_revoke_access(ctx, user_grp, repo_grp, user, token):
        raise Exit(1)

@github.command(name='check-invites')
@click.option('--repo-grp', required=1, type=click.File(),
              help='Repository group to check for expired invitations')
@click.option('--remove / --no-remove', required=0, default=False,
              help='Remove users from repo if their invites are more than --days old')
@click.option('--days', required=1, type=int, default=30,
              help='Number of days of outstanding invites to check for')
@click.option('--token', help='Github api token for username', required=True)
@click.pass_obj
def check_invites(ctx, repo_grp, remove, days, token):
    ''' Check repositories for invitations that have not been accepted. '''
    from dcf.cli.github import github_check_invites
    if not github_check_invites(ctx, repo_grp, remove, days, token):
        raise Exit(1)

@github.command()
@click.option('--src', required=0,
              help='Template repo name from which to copy - ex: user/repo1')
@click.option('--src-token', required=1, help='Github token for user who owns src-repo')
@click.option('--tgt', required=1,
              help='Target repository name - just the repo name, e.g. user/repo1 ')
@click.option('--tgt-token', required=1,
              help='Github password for user who owns (or will own) the target repo')
@click.option('--delete/--no-delete', required=0, default=True, show_default=True,
              help='Whether to delete labels on target repo before copying them from src-repo')
@click.option('--branches/--no-branches', required=0, default=True, show_default=True,
              help='Whether to create the develop and qa branches on the repo')
@click.option('--main-branch', required=0, default='master', show_default=True,
              help='Which branch is the current default branch in the tgt-repo')
@click.option('--default-branch', required=0, default='develop', show_default=True,
              help='Which branch to make the default branch in the tgt-repo')
@click.option('--create/--no-create', required=0, default=True, show_default=True,
              help='Whether to create the new repo or assume it already exists')
@click.pass_obj
def create_repo(ctx, src, src_token, tgt, tgt_token,
                delete, branches, main_branch, default_branch, create):
    """
        Either creates a new repo or instruments an existing repo with labels and branches.
        Copies labels from src-repo to tgt-repo.
    """
    from dcf.cli.github import github_create_repo
    if tgt in  ['loyaltymethods/rle-api', 'loyaltymethods/rle-ui']:
        raise click.UsageError('Target can not be set to ${tgt}')
    if not github_create_repo(ctx, src, src_token, tgt, tgt_token,
                              delete, branches, main_branch, default_branch, create):
        raise Exit(1)

@github.command()
@click.argument('collabname')
@click.option('--token', help='Github api token for username who owns repositories', required=True)
@click.pass_obj
def revoke_access_for_collab(ctx, collabname, token):
    ''' Revoke access to collaborator for repositories '''
    from dcf.cli.github import github_revoke_access_for_collab
    if not github_revoke_access_for_collab(ctx, collabname, token):
        raise Exit(1)
