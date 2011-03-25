============
Installation
============

Requirements
============
* `Sphinx <http://sphinx.pocoo.org/>`_ 1.0 or newer.

Installing
==========
* To install from source:

  The latest version of cloud_sptheme can be downloaded from `bitbucket <https://bitbucket.org/ecollins/cloud_sptheme>`_.
  Once downloaded and extracted, it can be installed using ``setup.py``::

    python setup.py build
    sudo python setup.py install

Documentation
=============
The latest copy of this documentation should always be available
at the `cloud_sptheme homepage <http://www.assurancetechnologies.com/software/cloud_sptheme>`_.

If you wish to generate your own copy of the documentation,
you will need to:

* install `Sphinx <http://sphinx.pocoo.org/>`_ (1.0 or better)
* download the cloud_sptheme source, and install cloud_sptheme itself.
* from the source directory, run ``python docs/make.py clean html``.
* Once Sphinx completes it's run, point a web browser to the file ``docs/_build/html/index.html``.
