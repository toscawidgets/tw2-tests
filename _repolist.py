#!/usr/bin/env python

import sys
import os
import shutil
import hashlib

NONE = '__none__'

bitbucket_repos = {
    # THIS IS UNBEARABLE.  TODO -- change to tw2.core
    'tw2dynforms' : 'paj',
    'tw2core' : 'ralphbean',
    'tw2.forms' : 'ralphbean',
    'tw2.jquery' : 'ralphbean',
    'tw2.sqla' : 'ralphbean',
    'tw2.devtools' : 'ralphbean',
    'tw2.jqplugins.elfinder' : 'josephtate',
    'tw2.jqplugins.elrte' : 'josephtate',
}
github_repos = {
    'tw2.jit' : 'ralphbean',

    'tw2.jqplugins.cookies' : 'ralphbean',
    'tw2.jqplugins.dynatree' : 'ralphbean',
    'tw2.jqplugins.fg' : 'ralphbean',
    'tw2.jqplugins.flot' : 'ralphbean',
    'tw2.jqplugins.jqgrid' : 'ralphbean',
    'tw2.jqplugins.jqplot' : 'ralphbean',
    'tw2.jqplugins.portlets' : 'ralphbean',
    'tw2.jqplugins.ui' : 'ralphbean',

    'tw2.polymaps' : 'ralphbean',
    'tw2.tipster' : 'ralphbean',

    'tw2.protovis.core' : 'ralphbean',
    'tw2.protovis.conventional' : 'ralphbean',
    'tw2.protovis.custom' : 'ralphbean',
    'tw2.protovis.hierarchies' : 'ralphbean',
    'tw2.etc' : 'ralphbean',
    'tw2.excanvas' : 'ralphbean',
}

# TODO -- just having tw2.forms here now for testing purposes
custom_repos = {
    'tw2.forms' : {
        'url' : 'https://bitbucket.org/toscawidgets/tw2.forms',
        'vcs' : 'mercurial',
        'clone_url' : 'https://bitbucket.org/toscawidgets/tw2.forms',
    },
    'tw2.core' : {
        'url' : 'https://bitbucket.org/toscawidgets/tw2.core',
        'vcs' : 'mercurial',
        'clone_url' : 'https://bitbucket.org/toscawidgets/tw2.core',
    }
}

class Repo(object):
    def __init__(self, service, project, account, url, vcs, clone_url):
        self.service = service
        if project[3] != '.':
            project = project[:3] + '.' + project[3:]
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
        self.tests = 'undefined'
        self.coverage = 'undefined'

    def gather_results(self):
        """ Should only be called after _run-tests.sh is called. """
        # Not very robust.
        with open('htmlcov/results-%s' % repr(self)) as f:
            lines = f.readlines()
            try:
                self.tests = lines[-3].strip()
            except IndexError as e:
                # Just for debugging this script.  This should never happen.
                self.tests = " <br/> ".join(lines)

        with open('htmlcov/summary.data') as f:
            lines = f.readlines()

        for line in lines:
            name, coverage = line.strip().split()
            if name == repr(self):
                self.coverage = coverage


    def __repr__(self):
        return '-'.join([
            self.name,
            self.account,
            self.service,
            hashlib.md5(self.clone_url).hexdigest()
        ])

    @property
    def name(self):
        return self.project

    @property
    def clone_command(self):
        return self.command + " " + self.clone_url + " " + repr(self)

    @property
    def test_command(self):
        commands = [
            "cd %s" % repr(self),
            "rmvirtualenv %s-venv" % repr(self),
            "mkvirtualenv --no-site-packages %s-venv" % repr(self),
            "pip install coverage",
            "python setup.py develop",
            "python setup.py test",
            "coverage run --source=tw2/ setup.py test",
            "COV=$(coverage report | tail -1 | awk ' { print $4 } ')",
            "python setup.py test -q 2>> ../htmlcov/results-%s" % repr(self),
            "coverage html",
            "mv htmlcov ../htmlcov/htmlcov-%s" % repr(self),
            "deactivate",
            "cd -",
            "notify-send '%s' \"$COV\"" % repr(self),
            "echo \"%s $COV\" >> htmlcov/summary.data" % repr(self),
        ]
        return " ;\n".join(commands)

repos = []

for k, v in bitbucket_repos.iteritems():
    repos.append(Repo(
        service='bitbucket',
        project=k,
        account=v,
        url='http://bitbucket.org/{v}/{k}'.format(v=v,k=k),
        vcs='mercurial',
        clone_url='http://bitbucket.org/{v}/{k}'.format(v=v,k=k),
    ))

for k, v in github_repos.iteritems():
    repos.append(Repo(
        service='github',
        project=k,
        account=v,
        url='http://github.com/{v}/{k}'.format(v=v,k=k),
        vcs='git',
        clone_url='https://github.com/{v}/{k}.git'.format(v=v,k=k)
    ))

for k, v in custom_repos.iteritems():
    repos.append(Repo(
        service=NONE,
        project=k,
        account=NONE,
        url=v['url'],
        vcs=v['vcs'],
        clone_url=v['clone_url'],
    ))

repos.sort(lambda r1, r2: cmp(r1.name, r2.name))

def destroy():
    """ rm -rf tw2* """
    print "#----"
    print "#Destroying."
    current_dir = '/'.join(__file__.split('/')[:-1])
    d, dirs, files = list(os.walk(current_dir))[0]
    for d in dirs:
        if not d.startswith('tw2'):
            print "# Ignoring directory", d
            continue
        print "# Removing", d
        shutil.rmtree(d)
    d, dirs, files = list(os.walk(current_dir+"/htmlcov/"))[0]
    for d in dirs:
        if not d.startswith('htmlcov'):
            print "# Ignoring directory", d
            continue
        d = 'htmlcov/'+d
        print "# Removing", d
        shutil.rmtree(d)
    for f in files:
        if f.startswith('results'):
            print "# Removing", f
            os.remove('htmlcov/'+f)
    try:
        os.remove('htmlcov/summary.data')
    except Exception as e:
        pass
    print "#Destroyed!"
    print "#----"

def clone():
    for repo in repos:
        print "# Clone", repr(repo)
        print repo.clone_command

def test():
    for repo in repos:
        print
        print "# Tests for", repr(repo)
        print repo.test_command


if __name__ == '__main__':
    print "#!/bin/bash -vx"
    print "source ~/.bashrc"
    print

    destroy()
    clone()
    test()

