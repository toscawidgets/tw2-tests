#!/usr/bin/env python

import datetime
import mako.template
import github2.client

ghc = github2.client.Github()

username = 'toscawidgets'

all_repos, page = [], 1
while True:
    new_repos = ghc.repos.list(username, page)
    if not new_repos:
        break
    all_repos += new_repos
    page += 1

link_tmpl = """
<img src="https://secure.travis-ci.org/{username}/{name}.png?branch={branch}">
</img>
"""

data = sorted([dict(
    repo=repo.name,
    master=link_tmpl.format(
        username=username,
        name=repo.name,
        branch='master'),
    develop=link_tmpl.format(
        username=username,
        name=repo.name,
        branch='develop'),
) for repo in all_repos
    if '-' not in repo.name],
    lambda a, b: cmp(a['repo'], b['repo']))

tmpl = """
<html>
<head>
<link rel='stylesheet' href='threebean.css' type='text/css'>
</head>
<body>
<div class="wrapper">
<h2><code>tw2</code> tests</h2>
<table>
<tr>
<th>github</th>
<th>pypi</th>
<th>demos</th>
<th>master</th>
<th>develop</th>
</tr>

% for row in data:
<tr>
<td><a href="http://github.com/${username}/${row['repo']}">${row['repo']}</a></td>
<td><a href="http://pypi.python.org/pypi/${row['repo']}">${row['repo']}</a></td>
<td><a href="http://tw2-demos.threebean.org/module?module=${row['repo']}">${row['repo']}</a></td>
<td>${row['master']}</td>
<td>${row['develop']}</td>
</tr>
% endfor
</table>
<div class="push"></div>
</div>
    <div class="footer">
    <p>This is a project of <a href="http://threebean.org">[three]Bean.org</a>.  Tests are
    run nightly.  Last generated at ${timestamp}.</p>
    <p>
    If you'd like to see your widget library listed on this page or the
    <a href="http://tw2-demos.threebean.org">demo page</a>, please email the
    <a href="http://groups.google.com/group/toscawidgets-discuss">toscawidgets-discuss</a> mailing list.</p>
    </div>

</body>
</html>
"""

template = mako.template.Template(tmpl)
print template.render(
    data=data,
    username=username,
    timestamp=datetime.datetime.isoformat(datetime.datetime.now())
)

