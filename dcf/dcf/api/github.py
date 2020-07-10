''' Classes for Github '''

from github import Github

class GithubAPI:
    ''' Class for Github API '''
    def __init__(self, config, token):

        self.config = config
        self.log = config.logger
        self.token = token
        if self.config.cli:
            self.log = config.console_logger
        self.server = Github(token)
        user = self.server.get_user()
        self.login = user.login

    def list_repositories(self):
        ''' List repositories in Github '''
        server = self.server
        try:
            return server.get_user().get_repos()
        except ConnectionError:
            self.log.info('Github Connection Error')
            return False
        except TimeoutError:
            self.log.info('Github Connect Timeout Error')
            return False
        except:
            self.log.info('Exception Occured during the API Call')
            return False

    def list_repos_for_collab(self, collab):
        ''' List Repositories for Collaborator '''
        server = self.server
        self.log.info('getting Repo list for this collaborator {}'.format(collab))
        repos = []
        try:
            for repo in server.get_user().get_repos():
                if repo.has_in_collaborators(collab) and repo not in repos:
                    repos.append(repo)
            return repos
        except ConnectionError:
            self.log.info('Github Connection Error')
            return False
        except TimeoutError:
            self.log.info('Github Connect Timeout Error')
            return False
        except:
            self.log.info('Exception Occured during the API Call')
            return False

    def readEntries(self, file_handle):
        ''' read all lines from a file '''
        return [line.rstrip('\n') for line in file_handle]

    def process_group_params(self, user_grp, repo_grp):
        ''' read the user/repo files and merge the creds dictionary with environment '''

        # Grab owners from repo group and look for passwords
        repos = self.readEntries(repo_grp)

        # Store context for next commands
        if user_grp:
            users = self.readEntries(user_grp)
        else:
            users = []
        return users, repos


    def grant(self, user_grp, repo_grp, user):
        '''  Grant access on a group of repos for a group of users '''
        server = self.server
        users, repos = self.process_group_params(user_grp, repo_grp)
        if user and user not in users:
            users.append(user)

        for repo in repos:
            self.log.info(f'Processing repo {repo}...')
            gh_repo = server.get_repo(repo)
            collaborators = set([c.login for c in gh_repo.get_collaborators()])
            new_collaborators = list(set(users) - collaborators)
            if new_collaborators:
                for collab in new_collaborators:
                    gh_repo.add_to_collaborators(collab, 'push')
                    self.log.info(f'Adding user {collab} to {repo}')
            else:
                self.log.info(f'There were no new collaborators to add in {repo}')

    def revoke(self, user_grp, repo_grp, user):
        ''' Revoke access on a group of repos for a group of users '''
        server = self.server
        users, repos = self.process_group_params(user_grp, repo_grp)
        if user and user not in users:
            users.append(user)

        for repo in repos:
            self.log.info(f'Processing repo {repo}...')
            gh_repo = server.get_repo(repo)
            collaborators = set([c.login for c in gh_repo.get_collaborators()])
            collaborators_to_remove = list(set(users).intersection(collaborators))
            if collaborators_to_remove:
                for collab in collaborators_to_remove:
                    self.log.info(f'Removing user {collab} from  {repo}')
                    gh_repo.remove_from_collaborators(collab)
            else:
                self.log.info(f'There were no matching collaborators in {repo}')

    def get_invitations(self, repo, days):
        ''' Get Invitations for the repositories who has not accepted '''
        server = self.server
        gh_repo = server.get_repo(repo)
        return gh_repo, gh_repo.get_pending_invitations()

    def get_labels(self, repo):
        ''' Get Labels for a repository '''
        server = self.server
        gh_repo = server.get_repo(repo)
        return gh_repo.get_labels()

    def create_repo(self, tgt, create):
        ''' Create Repo '''
        server = self.server
        if create:
            self.log.info(f'Creating Repo {tgt}...')
            trepo = tgt.split('/')[1]
            tgt_repo = server.get_user().create_repo(
                name=trepo,
                private=True,
                has_issues=True,
                has_wiki=True,
                has_downloads=True,
                has_projects=False,
                auto_init=True
            )
        else:
            tgt_repo = server.get_repo(tgt)
        return tgt_repo

    def delete_labels(self, delete, tgt, gh_repo):
        ''' Delete labels for a repository '''
        if delete:
            self.log.info('Deleteing all labels from {} repository...'.format(tgt))
            for label in gh_repo.get_labels():
                label.delete()
    def copy_labels(self, src_labels, gh_repo):
        ''' Copy Labels from Source to Target Repository '''
        # Copy the labels over
        existingLabels = []
        for label in gh_repo.get_labels():
            existingLabels.append(label.name)
        print('Copying labels...')
        for slabel in src_labels:
            if not slabel.name in existingLabels:
                self.log.info('Copying label "{}"'.format(slabel.name))
                gh_repo.create_label(slabel.name, slabel.color)

    def revoke_by_collab(self, repos, collabname):
        ''' Revoke access to repositories by collaborator '''
        server = self.server
        login = self.login
        for repo in repos:
            repoowner = repo.owner.login
            if repoowner == login:
                self.log.info(f'Processing repo {repo.name}...')
                try:
                    reponame = login + '/' + repo.name
                    gh_repo = server.get_repo(reponame)
                    if not repo.archived:
                        self.log.info(f'Removing user {collabname} from  {repo.name}')
                        gh_repo.remove_from_collaborators(collabname)
                except AssertionError:
                    self.log.info("Error occured in removing the collaborator")
