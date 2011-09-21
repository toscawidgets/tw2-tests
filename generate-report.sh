#!/bin/bash -e
source ~/.bashrc

if [ ! -f ~/finalize_report/bin/activate ] ; then
    virtualenv --no-site-packages ~/finalize_report
fi
source ~/finalize_report/bin/activate

pip install mako genshi mercurial formencode

./_repolist.py > _run-tests.sh
chmod +x _run-tests.sh

./_run-tests.sh

hg clone https://bitbucket.org/ralphbean/tw2.devtools || echo "Not cloning."
cd tw2.devtools ; python setup.py install ; cd -
./_finalize_report.py
deactivate
rm -rf ~/webapps/tw2_tests/*
cp htmlcov/index.html ~/webapps/tw2_tests/.
cp htmlcov/threebean.css ~/webapps/tw2_tests/.
mv htmlcov/htmlcov* ~/webapps/tw2_tests/.
mv htmlcov/results* ~/webapps/tw2_tests/.
find ~/webapps/tw2_tests/results* -exec mv {} {}.txt \;
