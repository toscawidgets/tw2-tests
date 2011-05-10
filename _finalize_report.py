#!/usr/bin/python

import mako.template

from _repolist import repos

# API Design ANTI-PATTERN.  Don't look at this.  :)
from tw2.devtools.browser import WbPage as page
import tw2.core.core
from tw2.core import make_middleware

tmpl_str = """
<html>
<head>
<link rel='stylesheet' href='threebean.css' type='text/css'>
<script type="text/javascript" src="http://vis.stanford.edu/protovis/protovis-r3.2.js"></script>
</head>
<body>
<div class="wrapper">
<h2><code>tw2</code> tests</h2>
<table>
<tr>
    <th>Repo</th>
    <th>Demo</th>
    <th>Module</th>
    <th>Commits</th>
    <th>Service</th>
    <th>Account</th>
    <th>Coverage</th>
    <th>Tests</th>
</tr>
% for r in repos:
<tr>
    <td><a href="${r.url}">[repo]</a></td>
    <td><a href="http://tw2-demos.threebean.org/module?module=${r.name}">[demo]</a></td>
    <td>${r.name}</td>
    <td>${sparkwidget(module=r.name).display() |n}</td>
    <td>${r.service}</td>
    <td>${r.account}</td>
    <td><a href="htmlcov-${repr(r)}/index.html">${r.coverage}</a></td>
    <td>${r.tests}</td>
</tr>
% endfor
</table>
<div class="push"></div>
</div>
    <div class="footer">
    <p>A project of <a href="http://threebean.org">[three]Bean.org</a>.  Tests are
    run nightly.</p>
    <p>
    If you'd like to see your widget library listed on this page or the<br/>
    <a href="http://tw2-demos.threebean.org">demo page</a>, please email the
    <a href="http://groups.google.com/group/toscawidgets-discuss">toscawidgets-discuss</a> mailing list.</p>
    </div>
</body>
</html>
"""

if __name__ == '__main__':
    # Ridiculous hack :/
    rl = tw2.core.core.request_local()
    rl.clear()
    rl['middleware'] = make_middleware()
    page = page.req()

    for r in repos:
        r.gather_results()
    template = mako.template.Template(tmpl_str)
    output = template.render(repos=repos, sparkwidget=page.commits)
    with open('htmlcov/index.html', 'w') as f:
        f.write(output)

