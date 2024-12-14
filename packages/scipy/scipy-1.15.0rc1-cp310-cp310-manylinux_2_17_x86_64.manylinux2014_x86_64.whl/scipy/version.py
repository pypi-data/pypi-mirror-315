
"""
Module to expose more detailed version info for the installed `scipy`
"""
version = "1.15.0rc1"
full_version = version
short_version = version.split('.dev')[0]
git_revision = "ba8553c12cfa4d3ee3df1f862230f360638dd64c"
release = 'dev' not in version and '+' not in version

if not release:
    version = full_version
