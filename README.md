# Twempest
Twitter to text via template. Somehow that abbreviates to "twempest".

[![status](https://img.shields.io/pypi/status/Twempest.svg)](https://pypi.python.org/pypi/twempest/)
[![buildstatus](https://travis-ci.org/yukondude/Twempest.svg?branch=master)](https://travis-ci.org/yukondude/Twempest)
[![codecov](https://codecov.io/gh/yukondude/Twempest/branch/master/graph/badge.svg)](https://codecov.io/gh/yukondude/Twempest)
[![pypiversion](https://img.shields.io/pypi/v/Twempest.svg)](https://pypi.python.org/pypi/twempest/)
[![pyversions](https://img.shields.io/pypi/pyversions/Twempest.svg)](https://pypi.python.org/pypi/twempest/)
[![licence](https://img.shields.io/pypi/l/Twempest.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html)

## Motivation

Twempest was born of the need to periodically echo my Twitter tweets as posts on my Jekyll-built blog.
That's it, that's all.

## Licence

Licensed under the [GNU General Public License, version 3](https://www.gnu.org/licenses/gpl-3.0.en.html).
Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

## Change Log

The current version is 0.1.1.
Twempest is [semver](http://semver.org/)-ish in its versioning scheme.

Twempest is currently an alpha release, so expect many many breaking changes.

## Installation

### Homebrew (macOS)

On macOS, Homebrew will take care of installing any dependencies, including Python 3.

    brew tap yukondude/tap
    brew install twempest

### PyPI (POSIX)

On *NIX, you will first need to install Python 3.3 (or higher) using your preferred method.

    pip3 install twempest

## Development Setup

 1. Create a Python 3 virtualenv for Twempest: `mkvirtualenv --python=$(which python3) Twempest`
 1. Clone the Twempest repo: `git clone https://github.com/yukondude/Twempest.git`
 1. Install dependencies: `pip install -r requirements.txt -r requirements-dev.txt -r requirements-test.txt`
 1. Install the project in development mode: `./setup.py develop`
 1. Run the unit tests to make sure everything is copacetic: `./setup.py test`
 1. Pour a snifter of Château de Montifaud and light up a Laranja Reserva Toro.

## Usage
Run `twempest --help` to view the usage instructions:

```
Usage: twempest [OPTIONS] TEMPLATE

  Download a sequence of recent Twitter tweets and convert these, via the
  given template file, to text format.

Options:
  -c, --config-path TEXT  Twempest configuration directory path. The
                          twempest.conf file must exist in this location.
                          [default: ~/.twempest]
  -f, --render-file TEXT  The file name (template tags allowed) for the
                          rendered tweets. If omitted, tweets will be rendered
                          to STDOUT.
  -p, --render-path TEXT  The directory path (template tags allowed) to write
                          the rendered tweets.  [default: .]
  -@, --replies           Include @replies in the list of retrieved tweets.
  -r, --retweets          Include retweets in the list of retrieved tweets.
  -V, --version           Show version and exit.
  -h, --help              Show this message and exit.
```

## Sample Configuration
Contents of `twempest.config.sample`:

```
# Sample Twempest configuration file. See https://github.com/yukondude/Twempest
# for details. Save this to ~/.twempest/twempest.config as the default
# configuration whenever twempest is run, or save it somewhere convenient as
# twempest.config and reference it via the -c/--config-path command-line switch.

[twempest]
# Most twempest long-form command-line switches may be used here (excluding the
# leading double-dash). The obvious exceptions would include --config-path,
# --help, and --version, but go ahead and try them if you like. The defaults
# are shown below, commented out. See the --help output for details.

# Render tweets to STDOUT.
# render-file=
# Because template expressions are allowed for this option, you can generate
# rendered file names using any of the tweet context variable contents. For
# example:
# render-file={{tweet.created_at|isodate}}-{{tweet.text|slugify}}.md
# might render to something like the following: 2017-02-14-be-my-valentine.md
# Use the slugify filter to eliminate any non-filesystem-safe characters from
# the tweet text.

# Write rendered tweets to the current directory.
# render-path=.

# Exclude @replies from the list of retrieved tweets.
# replies=false

# Exclude retweets from the list of retrieved tweets.
# retweets=false

[twitter]
# Visit https://apps.twitter.com/ to generate these keys, secrets, tokens, and
# token secrets. Secret tokens? Token keys? Secret secrets?
consumer_key=
consumer_secret=
access_token=
access_token_secret=
```

## Sample Template
A simple template to render a tweet as Markdown text (`twempest.template.sample`):

```
#{{ tweet.text|scrub|truncate(80,False) }}
Tweeted by: {{ tweet.user.screen_name }}
Tweeted at: {{ tweet.created_at }}
Tweet ID: {{ tweet.id }}
Tweet Entities:
{{ tweet.entities|pprint }}

{{ tweet.text }}
```

*README.md generated February 21, 2017*
