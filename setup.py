"""
cloud_sptheme setup script
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
    name = "cloud_sptheme",
    version = "1.0",
    author = "Eli Collins",
    author_email = "elic@assurancetechnologies.com",
    description = "a nice sphinx theme, and some related extensions",
    license = "BSD",
    keywords = "sphinx extension theme",
    url = "https://bitbucket.org/ecollins/cloud_sptheme",
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        #there should be a Framework::Sphinx::Extension classifier :)
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Software Development :: Documentation',
    ]
)
#=========================================================
#EOF
#=========================================================
