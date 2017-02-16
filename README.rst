Twempest
========

|status| |buildstatus| |codecov| |pypiversion| |pyversions| |licence|

Motivation
----------

Twempest was born of the need to periodically echo my Twitter tweets as
posts on my Jekyll-built blog. That's it, that's all.

Licence
-------

Licensed under the `GNU General Public License, version
3 <https://www.gnu.org/licenses/gpl-3.0.en.html>`__. Refer to the
attached LICENSE file or see http://www.gnu.org/licenses/ for details.

Change Log
----------

The current version is 0.1.1. Twempest is
`semver <http://semver.org/>`__-ish in its versioning scheme.

Twempest is currently an alpha release, so expect many many breaking
changes.

Installation
------------

Homebrew (macOS)
~~~~~~~~~~~~~~~~

On macOS, Homebrew will take care of installing any dependencies,
including Python 3.

::

    brew tap yukondude/tap
    brew install twempest

PyPI (POSIX)
~~~~~~~~~~~~

On \*NIX, you will first need to install Python 3.3 (or higher) using
your preferred method.

::

    pip3 install twempest

Development Setup
-----------------

1. Create a Python 3 virtualenv for Twempest:
   ``mkvirtualenv --python=$(which python3) Twempest``
2. Clone the Twempest repo:
   ``git clone https://github.com/yukondude/Twempest.git``
3. Install dependencies:
   ``pip install -r requirements.txt -r requirements-dev.txt -r requirements-test.txt``
4. Install the project in development mode: ``./setup.py develop``
5. Run the unit tests to make sure everything is copacetic:
   ``./setup.py test``
6. Pour a snifter of Château de Montifaud and light up a Laranja Reserva
   Toro.

Usage
-----

::

    Usage: twempest [OPTIONS]

      Download a sequence of recent Twitter tweets and convert these, via
      template, to text format.

    Options:
      -c, --config-path TEXT  Twempest configuration directory path. The
                              twempest.conf file must exist in this location.
                              [default: ~/.twempest]
      -@, --replies           Include @replies in the list of retrieved tweets.
      -r, --retweets          Include retweets in the list of retrieved tweets.
      -V, --version           Show version and exit.
      -h, --help              Show this message and exit.

*README.md generated February 16, 2017*

.. |status| image:: https://img.shields.io/pypi/status/Twempest.svg
   :target: https://pypi.python.org/pypi/twempest/
.. |buildstatus| image:: https://travis-ci.org/yukondude/Twempest.svg?branch=master
   :target: https://travis-ci.org/yukondude/Twempest
.. |codecov| image:: https://codecov.io/gh/yukondude/Twempest/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/yukondude/Twempest
.. |pypiversion| image:: https://img.shields.io/pypi/v/Twempest.svg
   :target: https://pypi.python.org/pypi/twempest/
.. |pyversions| image:: https://img.shields.io/pypi/pyversions/Twempest.svg
   :target: https://pypi.python.org/pypi/twempest/
.. |licence| image:: https://img.shields.io/pypi/l/Twempest.svg
   :target: https://www.gnu.org/licenses/gpl-3.0.en.html
