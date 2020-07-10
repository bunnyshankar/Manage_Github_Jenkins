''' Github Functions '''

from datetime import datetime
import sys
import prettytable

def connect_github(ctx, token):
    ''' To Connnect to Github Server '''
    print('Connecting to Github Server...')
    from dcf.api.github import GithubAPI
    return GithubAPI(ctx, token)

def list_github_repos(ctx, token):
    ''' List Repositories in Github '''
    api = connect_github(ctx, token)
    print('Listing the Repositories...')
    repos = api.list_repositories()
    if not repos:
        sys.exit("No Repos Found")
    repo_table = prettytable.PrettyTable(
        ['Repositories']
    )
    repo_table.align['Repositories'] = 'l'
    repo_table.hrules = prettytable.ALL
    for repo in repos:
        login = repo.owner.login
        repo_table.add_row([
            login+'/'+repo.name
        ])
    print(repo_table)

def list_collab_repos(ctx, collabname, token):
    ''' List Repositories for a user '''
    api = connect_github(ctx, token)
    repos = api.list_repos_for_collab(collabname)
    if not repos:
        sys.exit("No Repos Found")
    repo_table = prettytable.PrettyTable(
        ['Repositories']
    )
    repo_table.align['Repositories'] = 'l'
    repo_table.hrules = prettytable.ALL
    for repo in repos:
        login = repo.owner.login
        repo_table.add_row([
            login+'/'+repo.name
        ])
    print(repo_table)

def github_repo_access(ctx, user_grp, repo_grp, user, token):
    ''' Grant Access to repositor(ies) for user(s) '''
    api = connect_github(ctx, token)
    api.grant(user_grp, repo_grp, user)

def  github_revoke_access(ctx, user_grp, repo_grp, user, token):
    ''' Revoke Access to repositor(ies) for user(s) '''
    api = connect_github(ctx, token)
    api.revoke(user_grp, repo_grp, user)

def github_check_invites(ctx, repo_grp, remove, days, token):
    ''' Check repositories for invitations that have not been accepted. '''
    api = connect_github(ctx, token)
    users, repos = api.process_group_params(None, repo_grp)
    for repo in repos:
        gh_repo, invitations = api.get_invitations(repo, days)
        for invite in invitations:
            inviteid = invite.id
            created = invite.created_at
            name = invite.invitee.login
            current = datetime.utcnow()
            age = (current - created).days
            #age = td.days
            if age > days:
                print("User {} has invite for this repo {} since {} that's {} days."
                      .format(name, repo, created, age))
                if remove:
                    print("Revoking invitation for this user {} from {}".format(name, repo))
                    gh_repo.remove_invitation(inviteid)

def github_create_repo(ctx, src, src_token, tgt, tgt_token,
                       delete, branches, main_branch, default_branch, create):
    ''' Create repo or instruments repo '''
    api = connect_github(ctx, src_token)
    src_labels = api.get_labels(src)
    tapi = connect_github(ctx, tgt_token)
    gh_repo = tapi.create_repo(tgt, create)
    tapi.delete_labels(delete, tgt, gh_repo)
    print('Getting labels from {} repository...'.format(src))
    tapi.copy_labels(src_labels, gh_repo)
    # Create a develop and qa branch
    if branches:
        print('Creating develop, master and qa branches...')

        branchref = gh_repo.get_branch(main_branch)
        branches = ['master', 'develop', 'qa']
        branches.remove(main_branch)
        for branch in branches:
            print('Creating {}...'.format(branch))
            refs = 'refs/heads/' + branch
            gh_repo.create_git_ref(ref=refs, sha=branchref.commit.sha)
        print('Setting develop as default branch...')
        gh_repo.edit(default_branch=default_branch)

def github_revoke_access_for_collab(ctx, collabname, token):
    ''' REvoke access to a collaborator '''
    api = connect_github(ctx, token)
    repos = api.list_repos_for_collab(collabname)
    api.revoke_by_collab(repos, collabname)
        #gh_repo.remove_from_collaborators(collabname)
        #login = repo.owner.login
        #repo_table.add_row([
        #    login+'/'+repo.name
        #])
