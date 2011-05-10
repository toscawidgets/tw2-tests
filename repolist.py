#!/usr/bin/env python

import sys
import os
import shutil

bitbucket_repos = {
    'tw2.core' : 'toscawidgets',
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
        return 'cd %s ; python setup.py nosetests ; cd -' % self.name

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
    d, dirs, files = list(os.walk('/'.join(__file__.split('/')[:-1])))[0]
    for d in dirs:
        if not d.startswith('tw2'):
            print "Ignoring directory", d
            continue
        shutil.rmtree(d)

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

