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

The current version is 0.1.2. Twempest is
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

Run ``twempest --help`` to view the usage instructions:

::

    Usage: twempest [OPTIONS] TEMPLATE

      Download a sequence of recent Twitter tweets and convert these, via the
      given template file, to text format. Twempest uses the Jinja template
      syntax throughout: http://jinja.pocoo.org/docs/2.9/templates/

    Options:
      -c, --config-path TEXT  Twempest configuration directory path, which must be
                              writable, and must also contain the twempest.conf
                              file.  [default: ~/.twempest]
      -a, --append            Append rendered tweet(s) to existing file(s) rather
                              than skipping past with a warning.
      -i, --image-path TEXT   The directory path (template tags allowed) to write
                              downloaded image (media type == 'photo') files. The
                              directory path will be created if it doesn't exist.
                              Media file names use the --render-file name followed
                              by a number and the appropriate file extension. If
                              omitted, media files will not be downloaded.
      -u, --image-url TEXT    The URL path (template tags allowed) to use for all
                              image files downloaded via the --image-path option.
      -f, --render-file TEXT  The file name (template tags allowed) for the
                              rendered tweets. If omitted, tweets will be rendered
                              to STDOUT.
      -p, --render-path TEXT  The directory path (template tags allowed) to write
                              the rendered tweet files. The directory path will be
                              created if it doesn't exist.  [default: .]
      -@, --replies           Include @replies in the list of retrieved tweets.
      -r, --retweets          Include retweets in the list of retrieved tweets.
      -s, --since-id TEXT     Retrieve tweets that follow this ID in the timeline.
                              Required, unless the ID has already been recorded in
                              the config path directory after a previous run of
                              Twempest.
      -V, --version           Show version and exit.
      -h, --help              Show this message and exit.

Sample Configuration
--------------------

Contents of ``twempest.config.sample``:

::

    # Sample Twempest configuration file. See https://github.com/yukondude/Twempest
    # for details. Save this to ~/.twempest/twempest.config as the default
    # configuration whenever twempest is run, or save it somewhere convenient as
    # twempest.config and reference it via the -c/--config-path command-line switch.

    [twempest]
    # Most twempest long-form command-line switches may be used here (excluding the
    # leading double-dash). The obvious exceptions would include --config-path,
    # --help, and --version, but go ahead and try them if you like. The commented-
    # out defaults are shown below. See the --help output for details.

    # Do not append to existing files.
    # append=false

    # Do not download image files.
    # image-path=

    # Do not download image files.
    # image-url=

    # Render tweets to STDOUT.
    # render-file=
    # Because template expressions are allowed for this option, you can generate
    # rendered file names using any of the tweet context variable contents. For
    # example: render-file={{tweet.created_at|isodate}}-{{tweet.text|slugify}}.md
    # might render to something like: 2017-02-14-be-my-valentine.md
    # Use the slugify filter to eliminate any non-filesystem-safe characters from
    # the tweet text.

    # Write rendered tweets to the current directory.
    # render-path=.
    # Template expressions are also allowed for this option, so the directory path
    # can be made to change based upon a tweet status variable.

    # Exclude @replies from the list of retrieved tweets.
    # replies=false

    # Exclude retweets from the list of retrieved tweets.
    # retweets=false

    # Don't specify a most recent Twitter ID.
    # since-id=
    # Since this isn't specified (and normally wouldn't be in a config file), there
    # must already be an ID recorded in the config path directory after a previous
    # run of Twempest.

    [twitter]
    # Visit https://apps.twitter.com/ to generate these keys, secrets, tokens, and
    # token secrets. Secret tokens? Token keys? Secret secrets?
    consumer_key=
    consumer_secret=
    access_token=
    access_token_secret=

Sample Template
---------------

A simple template to render a tweet as Markdown text suitable for Jekyll
posts (``twempest.template.sample``):

::

    ---
    title: {{ tweet.text|delink|truncate(80,False) }}
    author: {{ tweet.user.name }}
    date: '{{ tweet.created_at }}'
    tweet_id: {{ tweet.id }}
    ---
    {{ tweet.text|relink("[{{text}}]({{url}})")|reimage("![{{alt}}]({{url}})") }}

Template Filters
----------------

``delink``
~~~~~~~~~~

Remove URLs and hashtag '#' prefixes.

``isodate``
~~~~~~~~~~~

Format a date as YYYY-MM-DD.

``reimage(tag_format)``
~~~~~~~~~~~~~~~~~~~~~~~

Remove image URLs and append them to the end, using the template
tag\_format with variables ``alt`` and ``url`` to format each.

``relink(tag_format)``
~~~~~~~~~~~~~~~~~~~~~~

Replace non-image URLs and hashtag links, using the template tag\_format
with variables ``text`` and ``url`` to format each.

``slugify``
~~~~~~~~~~~

Transform the given text into a suitable file name that is also scrubbed
of URLs and hashtags.

*README.md generated February 26, 2017*

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
