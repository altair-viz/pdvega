#!/bin/bash

# get git hash for commit message
GITHASH=$(git rev-parse HEAD)
MSG="doc build for commit $GITHASH"
cd _build

# clone the repo if needed
if test -d pdvega;
then echo "using existing cloned pdvega directory";
else git clone git@github.com:jakevdp/pdvega.git;
fi

# sync the website
cd pdvega
git checkout gh-pages
git pull

# remove all tracked files
git ls-files -z | xargs -0 rm -f

# sync files from html build
rsync -r ../html/ ./

# ensure there is a nojekyl file for github pages
touch .nojekyll

# add commit, and push to github
git add . --all
git commit -m "$MSG"
git push origin gh-pages
