#!/bin/bash -e
source ~/.bashrc

workon finalize_report || mkvirtualenv --no-site-packages finalize_report
pip install mako genshi mercurial formencode

#./_repolist.py > _run-tests.sh
#chmod +x _run-tests.sh

#./_run-tests.sh

#hg clone https://bitbucket.org/ralphbean/tw2.devtools || echo "Not cloning."
#cd tw2.devtools ; python setup.py install ; cd -
./_finalize_report.py
deactivate
cp htmlcov/index.html ~/webapps/tw2_tests/.
cp htmlcov/threebean.css ~/webapps/tw2_tests/.
mv htmlcov/htmlcov* ~/webapps/tw2_tests/.
