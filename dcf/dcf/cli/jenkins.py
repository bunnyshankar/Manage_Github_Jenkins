''' Jenkin Functions '''

import prettytable

def connect_jenkins(ctx, user, token):
    ''' To Connnect to Jenkin Server '''
    print('Connecting to Jenkins Server...')
    from dcf.api.jenkins import JenkinsAPI
    return JenkinsAPI(ctx, user, token)

def list_jenkins_jobs(ctx, user, token):
    ''' List Job names in Jenkins Server '''
    api = connect_jenkins(ctx, user, token)
    print('Listing the jobs...')
    ignore = ['develop', 'qa', 'master', 'bug', 'feature', 'PR', 'hotfix', 'Misc-Test']
    jobs = api.list_jobs()
    job_table = prettytable.PrettyTable(
        ['Folder and JobNames']
    )
    job_table.align['Folder and JobNames'] = 'l'
    job_table.hrules = prettytable.ALL
    for jobnames in jobs:
        ignore_found = False
        name = jobnames['name']
        for item in ignore:
            if item in name:
                ignore_found = True
                break
        if not ignore_found: 
        #if "develop" not in name and "qa" not in name and "master" not in name and "bug" not in name and "feature" not in name and "PR" not in name:
            job_table.add_row([
                jobnames['fullname']
            ])
    print(job_table)


def add_github_branch(ctx, user, token, jobname, branchname):
    ''' Add Github branch to Jenkins Multi Branch pipeline Job '''
    api = connect_jenkins(ctx, user, token)
    api.add_branch_to_job(jobname, branchname)

def delete_github_branch(ctx, user, token, jobname, branchname):
    ''' Delete Github branch from Jenkins Multi Branch pipeline Job '''
    api = connect_jenkins(ctx, user, token)
    api.delete_branch_from_job(jobname, branchname)

def create_jenkins_job(ctx, user, token, foldername, reponame, script):
    ''' Creates a jenkins job '''
    api = connect_jenkins(ctx, user, token)
    api.create_jenkins_mbp_job(foldername, reponame, script)

def check_jenkins_job(ctx, user, token, jobname):
    ''' Check Job in Jenkins Server '''
    api = connect_jenkins(ctx, user, token)
    exists = api.check_job(jobname)
    if exists:
        print("Job {} exists in Jenkins Server".format(jobname))
    else:
        print("Job {} doesnot exist in Jenkins Server".format(jobname))

def get_build_history(ctx, user, token, jobname, branch):
    ''' Get Build Numbers from the Build History '''
    api = connect_jenkins(ctx, user, token)
    builds = api.get_build_numbers(jobname, branch)
    job_table = prettytable.PrettyTable(
        ['Build History']
    )
    job_table.align['Build History'] = 'l'
    job_table.hrules = prettytable.ALL
    for build in builds:
        job_table.add_row([
            build['number']
        ])
    print(job_table)

def get_build_console_log(ctx, user, token, jobname, branch, buildnumber):
    ''' Get Build Console Log '''
    api = connect_jenkins(ctx, user, token)
    api.get_build_log(jobname, branch, buildnumber)
