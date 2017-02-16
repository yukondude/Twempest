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

*README.md generated February 16, 2017*
