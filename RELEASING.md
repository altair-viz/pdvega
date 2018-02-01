1. Update version in pdvega/__init__.py to, e.g. 0.2

2. Update version in conf.py (in two places!)

3. Make sure CHANGES.md is up to date for the release

4. Commit change and push to master

       git add . -u
       git commit -m "MAINT: bump version to 0.2"
       git push origin master

5. Tag the release:

       git tag -a v0.2 -m "version 0.2 release"
       git push origin v0.2

6. publish to PyPI (Requires correct PyPI owner permissions)

       python setup.py sdist upload

7. Build and push the docs website:

       python setup.py install
       cd doc
       bash sync_website.sh

8. update version in pdvega/__init__.py to, e.g. 0.3.0dev0

9. update version in doc/conf.py (in two places!)

10. add a new changelog entry for the unreleased version

11. Commit change and push to master

       git add . -u
       git commit -m "MAINT: bump version to 0.3.0dev"
       git push origin master

    