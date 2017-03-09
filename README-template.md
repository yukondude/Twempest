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

The current version is @@VERSION@@.
Twempest is [semver](http://semver.org/)-ish in its versioning scheme.

Twempest is currently a beta release, so expect a few breaking changes.

## Installation

### Homebrew (macOS)

On macOS, Homebrew will take care of installing any dependencies, including Python 3.

    brew tap yukondude/tap
    brew install twempest

### PyPI (POSIX)

On *NIX, you will first need to install Python 3.6 (or higher) using your preferred method.

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
@@HELPTEXT@@
```

## Sample Configuration
Contents of `twempest.config.sample`:

```
@@CONFIGTEXT@@
```

## Sample Template
A simple template to render a tweet as Markdown text suitable for Jekyll posts (`twempest.template.sample`):

```
@@TEMPLATETEXT@@
```

The rendered output of this template might look something like the following:

```
---
title: 'Ice fog &#34;boiling&#34; up from the Yukon River.'
author: 'Dave Rogers'
date: '2016-12-06 12:12:36-08:00'
tweet_id: 806229878861201408
---
Ice fog "boiling" up from the [#Yukon](https://twitter.com/hashtag/yukon) River.
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

### `reimage(tag_format, delimiter=" ")`
Remove image URLs and append them to the end (following the delimiter), using the template tag_format with variables `alt` and `url` to
format each.

### `relink(tag_format)`
Replace non-image URLs, hashtag, and user mention links, using the template tag_format with variables `text` and `url` to format each.

### `slugify`
Transform the given text into a suitable file name that is also scrubbed of URLs and hashtags.

*README.md generated @@TODAY@@*
