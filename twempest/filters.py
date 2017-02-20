""" Twempest Jinja2 custom filters.
"""

# This file is part of Twempest. Copyright 2017 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import jinja2


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
