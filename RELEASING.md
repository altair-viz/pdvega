1. Update version in pdvega/__init__.py to, e.g. 0.2

2. Make sure CHANGES.md is up to date for the release

3. Commit change and push to master

       git add . -u
       git commit -m "MAINT: bump version to 0.2"
       git push origin master

4. Tag the release:

       git tag -a v0.2 -m "version 0.2 release"
       git push origin v0.2

5. publish to PyPI (Requires correct PyPI owner permissions)

       python setup.py sdist upload

6. update version in pdvega/__init__.py to, e.g. 0.3.0dev0

7. add a new changelog entry for the unreleased version

8. Commit change and push to master

       git add . -u
       git commit -m "MAINT: bump version to 0.3.0dev"
       git push origin master

    