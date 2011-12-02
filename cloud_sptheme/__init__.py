"""
This module contains a few small sphinx extensions.
They are mainly used to help with the generation
of BPS's own documentation, but some other projects
use them as well, so they are kept here.
"""
import re
import os.path

__version__ = "1.3.dev0"

def get_theme_dir():
    "return path to directory containing sphinx themes in this package"
    return os.path.abspath(os.path.join(__file__,os.path.pardir, "themes"))

def get_version(release):
    "derive short version string from longer release"
    return re.match("(\d+\.\d+)", release).group(1)

# names of standard cloud extensions
# used by most cloud themes
std_exts = [
    'cloud_sptheme.ext.autodoc_sections',
    'cloud_sptheme.ext.index_styling',
    'cloud_sptheme.ext.relbar_toc',
]

# names of all cloud extensions
all_exts = std_exts + [
    'cloud_sptheme.ext.issue_tracker',
    'cloud_sptheme.ext.escaped_samp_literals',
]
