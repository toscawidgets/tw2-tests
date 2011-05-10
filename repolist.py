#!/usr/bin/env python

import sys
import os
import shutil

bitbucket_repos = {
    # THIS IS UNBEARABLE.  TODO -- change to tw2.core
    'tw2core' : 'ralphbean',
}
github_repos = {
    'tw2.jit' : 'ralphbean',
}

# TODO -- just having tw2.forms here now for testing purposes
custom_repos = {
    'tw2.forms' : {
        'url' : 'https://bitbucket.org/toscawidgets/tw2.forms',
        'vcs' : 'mercurial',
        'clone_url' : 'https://bitbucket.org/toscawidgets/tw2.forms',
    }
}

class Repo(object):
    def __init__(self, service, project, account, url, vcs, clone_url):
        self.service = service
        self.project = project
        self.account = account
        self.url = url
        self.vcs = vcs
        self.clone_url = clone_url
        command_lookup = {
            'mercurial' : 'hg clone',
            'git' : 'git clone',
        }
        self.command = command_lookup[self.vcs]

    @property
    def name(self):
        return self.project

    @property
    def clone_command(self):
        return self.command + " " + self.clone_url

    @property
    def test_command(self):
        commands = [
            "cd %s" % self.name,
            "rmvirtualenv %s-venv" % self.name,
            "mkvirtualenv --no-site-packages %s-venv" % self.name,
            "pip install coverage",
            "python setup.py develop",
            "coverage run --source=tw2/ setup.py test",
            "COV=$(coverage report | tail -1 | awk ' { print $4 } ')",
            "coverage html",
            "mv htmlcov ../htmlcov/htmlcov-%s" % self.name,
            "deactivate",
            "cd -",
            "notify-send '%s' \"$COV\"" % self.name,
            "echo \"%s $COV\" >> htmlcov/index.html" % self.name,
        ]
        return " ; ".join(commands)

repos = {}

for k, v in bitbucket_repos.iteritems():
    repos[k] = Repo(
        service='bitbucket',
        project=k,
        account=v,
        url='http://bitbucket.org/{v}/{k}'.format(v=v,k=k),
        vcs='mercurial',
        clone_url='http://bitbucket.org/{v}/{k}'.format(v=v,k=k),
    )

for k, v in github_repos.iteritems():
    repos[k] = Repo(
        service='github',
        project=k,
        account=v,
        url='http://github.com/{v}/{k}'.format(v=v,k=k),
        vcs='git',
        clone_url='https://github.com/{v}/{k}.git'.format(v=v,k=k)
    )

for k, v in custom_repos.iteritems():
    repos[k] = Repo(
        service=' --- ',
        project=k,
        account=' --- ',
        url=v['url'],
        vcs=v['vcs'],
        clone_url=v['clone_url'],
    )

def destroy():
    """ rm -rf tw2* """
    print "Destroying."
    current_dir = '/'.join(__file__.split('/')[:-1])
    d, dirs, files = list(os.walk(current_dir))[0]
    for d in dirs:
        if not d.startswith('tw2'):
            print " Ignoring directory", d
            continue
        print " Removing", d
        shutil.rmtree(d)
    d, dirs, files = list(os.walk(current_dir+"/htmlcov/"))[0]
    for d in dirs:
        if not d.startswith('htmlcov'):
            print "Ignoring directory", d
            continue
        d = 'htmlcov/'+d
        print " Removing", d
        shutil.rmtree(d)
    print "Destroyed!"
    print "----"

def clone():
    for name, repo in repos.iteritems():
        print repo.clone_command

def test():
    for name, repo in repos.iteritems():
        print repo.test_command

def aggregate():
    pass

if __name__ == '__main__':
    destroy()
    clone()
    test()
    aggregate()

