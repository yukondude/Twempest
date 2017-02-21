""" Twempest Jinja2 custom filters.
"""

# This file is part of Twempest. Copyright 2017 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import re
import unicodedata

import jinja2


def isodate(date):
    """ Return the given date formatted as the ISO 8601 extended YYYY-MM-DD format.
    """
    return date.strftime('%Y-%m-%d')


@jinja2.contextfilter
def scrub(ctx, text):
    """ Remove URLs and hashtag '#' prefixes from the given text, using the contents of the context's tweet status object as a guide.
    """
    tweet_entities = ctx.parent['tweet'].entities

    for hashtag in tweet_entities.get('hashtags', []):
        text = text.replace('#' + hashtag['text'], hashtag['text'])

    for media in tweet_entities.get('media', []):
        text = text.replace(media['url'], '')

    for url in tweet_entities.get('urls', []):
        text = text.replace(url['url'], '')

    return text


WEIRD_CHARACTERS_RE = re.compile(r"[^\w\s-]")
MULTIPLE_DELIMITERS_RE = re.compile(r"[-\s]+")


@jinja2.contextfilter
def slugify(ctx, text):
    """ Transform the given text into a suitable file name that is also scrubbed of URLs and hashtags.

        The bulk of this method is adapted from the Django project utils/text.py source code file:
        https://github.com/django/django/blob/master/django/utils/text.py

        Copyright (c) Django Software Foundation and individual contributors. All rights reserved.
        License: https://github.com/django/django/blob/master/LICENSE
    """
    slug = scrub(ctx, text)
    slug = unicodedata.normalize('NFKD', slug).encode('ascii', 'ignore').decode('ascii')
    slug = WEIRD_CHARACTERS_RE.sub('', slug).strip().lower()
    return MULTIPLE_DELIMITERS_RE.sub('-', slug).strip('-')
