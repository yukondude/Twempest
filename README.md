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

Copyright 2017 Dave Rogers.
Licensed under the [GNU General Public License, version 3](https://www.gnu.org/licenses/gpl-3.0.en.html).
Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

## Change Log

The current version is 0.2.6.
Twempest is [semver](http://semver.org/)-ish in its versioning scheme.

Twempest is currently a beta release candidate in preparation for version 1.0.0.

## Installation

### Homebrew (macOS)

On macOS, Homebrew will take care of installing any dependencies, including Python 3.

    brew tap yukondude/tap
    brew install twempest

### PyPI (POSIX)

On *NIX, you will first need to install Python 3.6 (or higher) using your preferred method.

    pip3 install twempest
    
### Unicode Locale Configuration

If the Unicode locale is not configured in a particular environment (e.g., `cron`), you will see the following error:

    RuntimeError: Click will abort further execution because Python 3
    was configured to use ASCII as encoding for the environment.
    Consult http://click.pocoo.org/python3/for mitigation steps.
    
[To solve this](http://click.pocoo.org/5/python3/#python3-surrogates), you must explicitly export the Unicode locale in the environment.
For example, insert something like the following near the top of your `crontab` file:
 
    LC_ALL=en_CA.UTF-8
    LANG=en_CA.UTF-8

Use the locale appropriate for your language and region.
The error message should show the list of available locales.

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
  given template file, to text format. Twempest uses the Jinja template
  syntax throughout: http://jinja.pocoo.org/docs/2.9/templates/

Options:
  -c, --config-path TEXT  Twempest configuration directory path, which must be
                          writable, and must also contain the twempest.conf
                          file.  [default: ~/.twempest]
  -a, --append            Append rendered tweet(s) to existing file(s) rather
                          than skipping past with a warning.
  -n, --count TEXT        Maximum number of tweets to retrieve. The actual
                          number may be lower.  [default: 200]
  -D, --dry-run           Display all configuration options and template
                          contents without retrieving tweets.
  -i, --image-path TEXT   The directory path (template tags allowed) to write
                          downloaded image (media type == 'photo') files. The
                          directory path will be created if it doesn't exist.
                          Media file names use the --render-file name followed
                          by a number and the appropriate file extension. If
                          omitted, media files will not be downloaded.
  -u, --image-url TEXT    The URL path (template tags allowed) to use for all
                          image files downloaded via the --image-path option.
  --pickle                Serialize a list of the rendered tweet statuses as a
                          standard Python pickle byte stream. The stream will
                          be written to 'twempest.p' in the current working
                          directory.
  -q, --quiet             Suppress warning messages.
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
  -k, --skip TEXT         Skip any rendered tweets that contain this regular
                          expression pattern.
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
# --help, and --version, but go ahead and try them if you like. The commented-
# out defaults are shown below. See the --help output for details.

# Do not append to existing files.
# append=false

# Retrieve at most 200 tweets.
# count=200

# Retrieve tweets normally.
# dry-run=false

# Do not download image files.
# image-path=

# Do not download image files.
# image-url=

# Do not serialize the rendered tweets.
# pickle=false

# Do not suppress warning messages.
# quiet=false

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

# Don't skip any tweets.
# skip=

[twitter]
# Visit https://apps.twitter.com/ to generate these keys, secrets, tokens, and
# token secrets. Secret tokens? Token keys? Secret secrets?
consumer_key=
consumer_secret=
access_token=
access_token_secret=
```

## Sample Template
A simple template to render a tweet as Markdown text suitable for Jekyll posts (`twempest.template.sample`):

```
---
title: '{{ tweet.text|delink|truncate(80,False)|qescape }}'
author: '{{ tweet.user.name|qescape }}'
date: '{{ tweet.created_at }}'
tweet_id: {{ tweet.id }}
---
{{ tweet.text | relink("[{{ text }}]({{ url }})") | reimage("![{{ alt }}]({{ url }})", "\n\n") }}

[tweet](https://twitter.com/{{tweet.user.screen_name}}/status/{{ tweet.id }})
```

The rendered output of this template might look something like the following:

```
---
title: 'Ice fog &#39;boiling&#39; up from the Yukon River.'
author: 'Dave Rogers'
date: '2016-12-06 12:12:36-08:00'
tweet_id: 806229878861201408
---
Ice fog 'boiling' up from the [#Yukon](https://twitter.com/hashtag/yukon) River.

![2016-12-06-ice-fog-boiling-up-from-the-yukon-river-0](/media/2016-12-06-ice-fog-boiling-up-from-the-yukon-river-0.jpg)

[tweet](https://twitter.com/yukondude/status/806229878861201408)
```

## `tweet` Context Variable
See the [Twitter API documentation for tweets](https://dev.twitter.com/overview/api/tweets) for a list of all of the keys that can be found
under the `tweet` context variable (a dictionary).

A couple of other keys are also available:

### `tweet.media[].original_media_url`
The original value of the `media_url` key within the list of `media` items before any downloaded image URL rewriting took place.

### `tweet.media[].original_media_url_https`
The original value of the `media_url_https` key within the list of `media` items before any downloaded image URL rewriting took place.

## Template Filters
These are in addition to the [built-in Jinja2 filters](http://jinja.pocoo.org/docs/2.9/templates/#list-of-builtin-filters).

### `delink`
Remove URLs and hashtag '#' prefixes.

### `isodate`
Format a date as YYYY-MM-DD.

### `qescape`
Escape just single quote characters as HTML entities.

### `reimage(tag_format, delimiter=" ")`
Remove image URLs and append them to the end (following the delimiter), using the template tag_format with variables `alt` and `url` to
format each.

### `relink(tag_format)`
Replace non-image URLs, hashtag, and user mention links, using the template tag_format with variables `text` and `url` to format each.

### `slugify`
Transform the given text into a suitable file name that is also scrubbed of URLs and hashtags.

*README.md generated March 16, 2017*
