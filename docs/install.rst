============
Installation
============

Requirements
============
* `Sphinx <http://sphinx.pocoo.org/>`_ 1.0 or newer.

Installing
==========
* To install from source:

  The latest version of astdoc can be downloaded from the `astdoc homepage <http://www.assurancetechnologies.com/software/astdoc>`_.
  Once downloaded and extracted, it can be installed using ``setup.py``::

    python setup.py build
    sudo python setup.py install

Documentation
=============
The latest copy of this documentation should always be available
at the `astdoc homepage <http://www.assurancetechnologies.com/software/astdoc>`_.

If you wish to generate your own copy of the documentation,
you will need to:

* install `Sphinx <http://sphinx.pocoo.org/>`_ (1.0 or better)
* download the astdoc source, and install astdoc itself.
* from the source directory, run ``python docs/make.py clean html``.
* Once Sphinx completes it's run, point a web browser to the file ``docs/_build/html/index.html``.
