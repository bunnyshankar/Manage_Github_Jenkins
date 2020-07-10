''' Classes for Jenkins '''

import tempfile
import jenkins

class JenkinsAPI:
    ''' Class for Jenkins API '''
    def __init__(self, config, user, token):

        self.config = config
        self.log = config.logger
        self.user = user
        self.token = token
        if self.config.cli:
            self.log = config.console_logger
        self.server = jenkins.Jenkins(
            'https://jenkinsURL',
            username=user, password=token
        )

    def list_jobs(self):
        ''' List jobs configured in Jenkins Server '''
        server = self.server
        try:
            return server.get_jobs(folder_depth=None)
        except ConnectionError:
            self.log.info('Jenkins Connection Error')
            return False
        except TimeoutError:
            self.log.info('Jenkins Connect Timeout Error')
            return False
        except:
            self.log.info('Exception Occured during the API Call')
            return False

    def get_job_config(self, jobname):
        ''' get Job Configuration from Jenkins Server '''
        server = self.server
        fout = open("/tmp/config.xml", "w")
        self.log.info('Getting Job configuration for this Job {}'.format(jobname))
        try:
            fout.write(server.get_job_config(jobname))
        except ConnectionError:
            self.log.info('Jenkins Connection Error')
        except TimeoutError:
            self.log.info('Jenkins Connect Timeout Error')
        except:
            self.log.info('Exception Occured during the API Call')
        finally:
            fout.close()

    def set_job_config(self, jobname, config_data):
        ''' Set Job Configuration in Jenkins Server '''
        server = self.server
        self.log.info('Setting Job configuration for this Job {}'.format(jobname))
        try:
            server.reconfig_job(jobname, config_data)
        except ConnectionError:
            self.log.info('Jenkins Connection Error')
        except TimeoutError:
            self.log.info('Jenkins Connect Timeout Error')
        except:
            self.log.info('Exception Occured during the API Call')

    def add_branch_to_job(self, jobname, branchname):
        ''' Add Branch to Jenkins MultiBranch Pipeline '''
        self.get_job_config(jobname)
        rex = '<regex>^('
        branch = branchname
        newbranch = rex+branch+"|"
        fin = open("/tmp/config.xml", "rt")
        data = fin.read()
        if branch not in data:
            data = data.replace(rex, newbranch)
            self.set_job_config(jobname, data)
            self.log.info('Branch {} added to this Job {}'.format(branch, jobname))
        else:
            self.log.info(
                'Branch {} found in this Job {}. No Need to add again. Exiting....'
                .format(branch, jobname)
            )
        fin.close()

    def delete_branch_from_job(self, jobname, branchname):
        ''' Delete Branch from Jenkins MultiBranch Pipeline '''
        self.get_job_config(jobname)
        branch = branchname
        rex = branch+"|"

        fin = open("/tmp/config.xml", "rt")
        data = fin.read()
        if rex not in data:
            self.log.info('Branch {} not found in this Job {} exiting.....'.format(branch, jobname))
        else:
            data = data.replace(rex, "")
            self.set_job_config(jobname, data)
            self.log.info('Branch {} deleted from this Job {}'.format(branch, jobname))
        fin.close()

    def create_jenkins_mbp_job(self, foldername, reponame, script):
        ''' Create Multi Pipeline  Jenkins Job '''
        server = self.server
        jobname = foldername + '/' + reponame
        chkjob = self.check_job(jobname)
        if not chkjob:
	    #Add your jenkins job from which you need to copy. This is like template.
            self.get_job_config("folder/job") ##Change this
            fin = open("/tmp/config.xml", "rt")
            data = fin.read()
            data = data.replace("repo", reponame) #Replace repo name accordingly as per your template
            data = data.replace("repo", reponame) #Replace repo name accordingly as per your template
            data = data.replace("jenkinsfile", script) #repo jenkinsfile name accordingly as per your template
            try:
                server.create_job(jobname, data)
            except ConnectionError:
                self.log.info('Jenkins Connection Error')
            except TimeoutError:
                self.log.info('Jenkins Connect Timeout Error')
            except:
                self.log.info('Exception Occured during the API Call')
            else:
                self.log.info(
                    'Job {} created successfully in folder {}'
                    .format(reponame, foldername)
                )
            finally:
                fin.close()
        else:
            self.log.info('Job {} exists already in this Folder {}'.format(reponame, foldername))

    def check_job(self, jobname):
        ''' Check job Exist in Jenkins Server '''
        server = self.server
        try:
            job = server.job_exists(jobname)
        except ConnectionError:
            self.log.info('Jenkins Connection Error')
            return False
        except TimeoutError:
            self.log.info('Jenkins Connect Timeout Error')
            return False
        except:
            self.log.info('Exception Occured during the API Call')
            return False
        return job

    def get_build_numbers(self, jobname, branch):
        ''' Get Build Numbers from Build History '''
        server = self.server
        job = jobname + '/' + branch
        self.log.info(
            'Getting Build Numbers for this Branch {} in this Job {}'
            .format(branch, jobname)
        )
        try:
            return server.get_job_info(job)['builds']
        except ConnectionError:
            self.log.info('Jenkins Connection Error')
            return False
        except TimeoutError:
            self.log.info('Jenkins Connect Timeout Error')
            return False
        except:
            self.log.info('Exception Occured during the API Call')
            return False

    def get_build_log(self, jobname, branch, buildnumber):
        ''' Get Build log for a Job '''
        server = self.server
        job = jobname + '/' + branch
        fout = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        floc = fout.name
        self.log.info(
            'Getting Build log from this Branch {} for this build {}'
            .format(branch, buildnumber)
        )
        try:
            fout.write(server.get_build_console_output(job, buildnumber))
        except ConnectionError:
            self.log.info('Jenkins Connection Error')
        except TimeoutError:
            self.log.info('Jenkins Connect Timeout Error')
        except TypeError:
            self.log.info('Check the buildNumber properly. It should be Int')
        except:
            self.log.info('Exception Occured during the API Call')
        else:
            self.log.info('The build log {} is located at {}'.format(buildnumber, floc))
        finally:
            fout.close()
