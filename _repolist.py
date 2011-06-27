#!/usr/bin/env python

import sys
import os
import shutil
import hashlib

NONE = '__none__'

bitbucket_repos = {
    # THIS IS UNBEARABLE.  TODO -- change to tw2.core
    'paj' : [
        'tw2core',
        'tw2devtools',
        'tw2dynforms',
        'tw2forms',
        'tw2.sqla',
        'tw2yui',
    ],
    'ralphbean' : [
        'tw2core',
        'tw2.forms',
        'tw2.jquery',
        'tw2.sqla',
        'tw2.devtools',
    ],
    'tbatterii' : [
        'tw2core',
    ],
    'josephtate' : [
        'tw2.jqplugins.elfinder',
        'tw2.jqplugins.elrte',
        'tw2.upload',
    ],
    'toscawidgets' : [
        'tw2.core',
        'tw2.forms',
        'tw2.jqplugins.ui',
        'tw2.jquery',
        'tw2.jwysiwyg',
        'tw2.recaptcha',
    ],
}
github_repos = {
    'decause' : [
        'tw2.huBarcode',
    ],
    'ralphbean' : [
        'tw2.etc',
        'tw2.excanvas',
        'tw2.jit',
        'tw2.jqplugins.cookies',
        'tw2.jqplugins.dynatree',
        'tw2.jqplugins.fg',
        'tw2.jqplugins.flot',
        'tw2.jqplugins.jqgrid',
        'tw2.jqplugins.jqplot',
        'tw2.jqplugins.portlets',
        'tw2.jqplugins.ui',
        'tw2.polymaps',
        'tw2.protovis.core',
        'tw2.protovis.conventional',
        'tw2.protovis.custom',
        'tw2.protovis.hierarchies',
        'tw2.rrd',
        'tw2.slideymenu',
        'tw2.tipster',
    ],
}

# This is for repos hosted neither on github nor bitbucket.  One-offs.
custom_repos = {
# Syntax should look something like:
#    'tw2.forms' : [
#        {
#            'url' : 'https://bitbucket.org/toscawidgets/tw2.forms',
#            'vcs' : 'mercurial',
#            'clone_url' : 'https://bitbucket.org/toscawidgets/tw2.forms',
#        }
#    ],
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
        try:
            with open('htmlcov/results-%s' % repr(self)) as f:
                lines = f.readlines()
                try:
                    self.tests = lines[-3].strip()
                except IndexError as e:
                    # Just for debugging this script.  This should never happen.
                    self.tests = " <br/> ".join(lines)
        except IOError as e:
            pass

        with open('htmlcov/summary.data') as f:
            lines = f.readlines()

        for line in lines:
            try:
                name, coverage = line.strip().split()
            except ValueError as e:
                continue
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
            "pushd %s" % repr(self),
            "rmvirtualenv %s-venv" % repr(self),
            "mkvirtualenv --no-site-packages %s-venv" % repr(self),
            "pip install coverage",
            "python setup.py develop",
            "python setup.py test",
            "coverage run --source=tw2/ setup.py test",
            "COV=$(coverage report | tail -1 | awk ' { print $4 } ')",
            "python setup.py test -q 2>> ../htmlcov/results-%s" % repr(self),
            "coverage html --omit=*.kid --omit=*samples*",
            "mv htmlcov ../htmlcov/htmlcov-%s" % repr(self),
            "deactivate",
            "popd",
            "echo \"%s $COV\" >> htmlcov/summary.data" % repr(self),
        ]
        return " ;\n".join(commands)

repos = []

for username, projects in bitbucket_repos.iteritems():
    for project in projects:
        repos.append(Repo(
            service='bitbucket',
            project=project,
            account=username,
            url='http://bitbucket.org/{v}/{k}'.format(
                v=username, k=project),
            vcs='mercurial',
            clone_url='http://bitbucket.org/{v}/{k}'.format(
                v=username, k=project),
        ))

for username, projects in github_repos.iteritems():
    for project in projects:
        repos.append(Repo(
            service='github',
            project=project,
            account=username,
            url='http://github.com/{v}/{k}'.format(
                v=username, k=project),
            vcs='git',
            clone_url='https://github.com/{v}/{k}.git'.format(
                v=username, k=project),
        ))

for project, paramsets in custom_repos.iteritems():
    for paramset in paramsets:
        repos.append(Repo(
            service=NONE,
            project=project,
            account=NONE,
            url=paramset['url'],
            vcs=paramset['vcs'],
            clone_url=paramset['clone_url'],
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

