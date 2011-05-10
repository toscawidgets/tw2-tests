#!/bin/bash
source ~/.bashrc

#./_repolist.py > _run-tests.sh
#chmod +x _run-tests.sh
#./_run-tests.sh

workon finalize_report || mkvirtualenv --no-site-packages finalize_report
pip install mako
hg clone https://bitbucket.org/ralphbean/tw2.devtools
cd tw2.devtools ; python setup.py install ; cd -
./_finalize_report.py
deactivate

