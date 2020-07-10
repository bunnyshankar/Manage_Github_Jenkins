# DCF / DevOps Control Framework

## CLI Requirements and Installation

Python 3.6+ pip3 and virtualenv required. Run "source install" or ". install" in this directory to install.


## CLI activation

Run "source activate" or ". activate" to activate a previously installed environment.

## CLI Use

The 'devops' command is used to configure the Manage Jenkins, Github

```
$ devops --help
Usage: devops [OPTIONS] COMMAND [ARGS]...



Options:
  --quiet               Only output summary of actions
  --debug / --no-debug  Debug output
  -h, --help            Show this message and exit.

Commands:
  jenkins Jenkins administration commands
  github Github administration commands

$ devops --region us-west-2
Starting DevOps Control Framework Shell...
DevOps>
```

### Jenkins

To list jobs and folders in jenkins server:

```
$ devops jenkins list-jobs --user admin --token xxxxx
```

To check if a particular job exists in jenkins server:

```
$ devops jenkins check-job --user admin --token xxxxx --jobname "folder/jobname"
```

To check build number history for a job

```
$ devops jenkins get-build-history --user admin --token xxxxx --jobname "folder/jobname" feature-multi-arch
```

To check build log for a job

```
$ devops jenkins get-build-log --user admin --token xxxxx --jobname "folder/jobname" --buildnumber 959  develop
```

To add a brach to a job

```
$ devops jenkins add-branch --user admin --token xxxxx --jobname "folder/jobname" feature-mongo-export
```

To Delete a branch from a job

```
$ devops jenkins delete-branch --user admin --token xxxxx --jobname "folder/jobname" bug-cursor-problems
```

To create a job

```
$ devops jenkins create-job  --user admin --token xxxxx --foldername "foldername" --script Jenkinsfile.python  jobname
```

###Github

For Listing repositories

```
$ devops github list-repos --token 11111
```

For Listing repositories of a collaborator

```
$ devops github list-repos-for-collab --token 11111  xxx
```

For giving access to set of collaborators to set of repositories

```
$ devops github grant-access --user xxx --user-grp /root/user.txt --repo-grp /root/repo.txt --token 11111
```

For giving access to a collaborator for set of repositories

```
$ devops github grant-access --user xxx --repo-grp /root/repo.txt --token 11111
```

For revoking access for a set of collaboerators from set of repositories

```
$ devops github revoke-access  --user-grp /root/user.txt --repo-grp /root/repo.txt --token 11111
```

For  revoking access for a collaborator from set of repositories

```
$ devops github revoke-access --user xxx --repo-grp /root/repo.txt --token 11111
```

For revoking access for a collaborator  in repositories in which he is collaborating

```
$ devops github revoke-access-for-collab --token 11111   xxx
```

For checking invites for a set of repositoties

```
$ devops github check-invites --repo-grp /root/repo.txt --token 11111
```

For creating an new repo

```
$ devops github create-repo --src srcuser/srcrepotemplate --src-token 11111 --tgt user/repo --tgt-token 22222
```
