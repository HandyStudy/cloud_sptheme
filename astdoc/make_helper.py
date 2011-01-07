"""helper for quick cross-platform makefile for sphinx

TODO: this was hacked up really quickly, could use a facelift.
TODO: document usage
"""
#===============================================================
#imports
#===============================================================
#core
import logging; log = logging.getLogger(__name__)
import os,sys
from string import Template
import subprocess
#pkg
#local
__all__ = [
    "SphinxMaker",
]

#===============================================================
#misc helpers
#===============================================================
def sub(fmt, **kwds):
    if not kwds:
            kwds = globals()
    return Template(fmt).substitute(**kwds)

#===============================================================
#fs helpers
#===============================================================
joinpath = os.path.join

def abspath(*args):
    return os.path.abspath(joinpath(*args))

if hasattr(os.path, "realpath"):
    def realpath(*args):
        return os.path.realpath(joinpath(*args))
else:
    #probably windows - fake it best we can
    def realpath(*args):
        return os.path.normcase(os.path.abspath(joinpath(*args)))

def pathdir(path):
    return os.path.split(path)[0]

def clearpath(path):
    "recursively remove all contents of dir, but leave dir"
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            os.remove(joinpath(root, name))
        for name in dirs:
            os.rmdir(joinpath(root, name))

def rmpath(path):
    "drecursively delete path"
    if os.path.exists(path):
        if os.path.isdir(path):
            clearpath(path)
            os.rmdir(path)
        else:
            os.remove(path)

def ensuredirs(path):
    "ensure specified directory & all parents exist"
    if not os.path.isdir(path):
        os.makedirs(path)

#===============================================================
#main class
#===============================================================
class SphinxMaker(object):
    #===============================================================
    #class attrs
    #===============================================================
    # You can subclass these variables
    #TODO: cmd line override support
    SPHINXOPTS    = []
    SPHINXBUILD   = "sphinx-build"
    PAPER         = "letter"

    # Paths
    BUILD = "_build"
    STATIC = "_static"

    #internal opts
    PAPEROPT_a4     = ["-D","latex_paper_size=a4"]
    PAPEROPT_letter = ["-D","latex_paper_size=letter"]
    #===============================================================
    #instance attrs
    #===============================================================
    root_dir = None
    conf_file = None
    conf = None

    #===============================================================
    #frontend
    #===============================================================
    def __init__(self, root_dir=None):
        if root_dir is None:
            root_dir = joinpath(sys.modules["__main__"].__file__, os.pardir)
        self.root_dir = abspath(root_dir)
        self.conf_file = joinpath(self.root_dir, "conf.py")
        if not os.path.exists(self.conf_file):
            raise RuntimeError, "conf file not found in root: %r" % (self.root_dir)
        #XXX: load conf file to learn extra params?

    @classmethod
    def execute(cls, args=None, **kwds):
        return cls(**kwds).run(args)

    def run(self, args=None):
        if args is None:
            args = sys.argv[1:]
        os.chdir(self.root_dir) #due to relative paths like self.BUILD
        for arg in args:
            getattr(self,"target_"+arg)()

    #===============================================================
    #targets
    #===============================================================
    def target_help(self):
        print "Please use \`make <target>' where <target> is one of"
        print "  clean     remove all compiled files"
        print "  html      to make standalone HTML files"
        print "  http      to serve standalone HTML files on port 8000"
#        print "  pickle    to make pickle files"
#        print "  json      to make JSON files"
        print "  htmlhelp  to make HTML files and a HTML help project"
#        print "  latex     to make LaTeX files, you can set PAPER=a4 or PAPER=letter"
#        print "  changes   to make an overview over all changed/added/deprecated items"
#        print "  linkcheck to check all external links for integrity"

    def target_clean(self):
        rmpath(self.BUILD)

    def target_html(self):
        #just in case htmldev was run
        rmpath(joinpath(self.BUILD, "html", "_static", "default.css"))
        self.build("html")

    def target_htmlhelp(self):
        self.build("htmlhelp")

    def target_http(self):
        self.target_html()
        path = realpath(self.BUILD, "html")
        os.chdir(path)
        port = 8000
        print "Serving files from %r on port %r" % (path, port)
        import SimpleHTTPServer as s
        s.BaseHTTPServer.HTTPServer(('',port), s.SimpleHTTPRequestHandler).serve_forever()

    ##def target_latex(self):
    ##    build("latex")
    ##    print "Run \`make all-pdf' or \`make all-ps' in that directory to" \
    ##        "run these through (pdf)latex."
    ##
    ##def target_pdf():
    ##    assert os.name == "posix", "pdf build support not automated for your os"
    ##    build("latex")
    ##    target = BUILD / "latex"
    ##    target.chdir()
    ##    subprocess.call(['make', 'all-pdf'])
    ##    print "pdf built"

    #===============================================================
    #helpers
    #===============================================================
    def build(self, name):
        BUILD = self.BUILD
        ALLSPHINXOPTS = self.get_sphinx_opts()
        
        dt = joinpath(BUILD, "doctrees")
        ensuredirs(dt)
        
        target = joinpath(BUILD, name)
        ensuredirs(target)
        
        rc = subprocess.call([self.SPHINXBUILD, "-b", name] + ALLSPHINXOPTS + [ target ])
        if rc:
            print "Sphinx-Build returned error, exiting."
            sys.exit(rc)
        print "Build finished. The %s pages are in %r." % (name, target,)
        return target

    def get_paper_opts(self):
        return getattr(self,"PAPER_" + self.PAPER, [])

    def get_sphinx_opts(self):
        return ["-d", joinpath(self.BUILD, "doctrees")] + self.get_paper_opts() + self.SPHINXOPTS + [ "." ]

    #===============================================================
    #eoc
    #===============================================================

#===============================================================
#eof
#===============================================================
