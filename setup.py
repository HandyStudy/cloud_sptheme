"""
astdoc setup script
"""
#=========================================================
#init script env
#=========================================================
import sys,os
from os.path import abspath, join
root_path = abspath(join(__file__, ".."))
os.chdir(root_path)
lib_path = '.'
#=========================================================
#imports
#=========================================================
from setuptools import setup, find_packages
#=========================================================
#setup
#=========================================================
setup(
    #package info
    packages = find_packages(where=lib_path),
    include_package_data = True,

    # metadata
    name = "astdoc",
    version = "1.0",
    author = "Eli Collins",
    author_email = "elic@astllc.org",
    description = "some useful sphinx extensions and additional themes used by Assurance Technologies",
    license = "BSD",
    keywords = "sphinx extension theme",
    url = "http://www.astllc.org/software/astdoc",
    # could also include long_description, download_url, classifiers, etc.
    zip_safe=False,
)
#=========================================================
#EOF
#=========================================================
