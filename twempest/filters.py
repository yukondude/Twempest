""" Twempest Jinja2 custom filters.
"""

# This file is part of Twempest. Copyright 2017 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.


def detweet(text, tweet):
    """ Remove URLs and hashtag '#' prefixes from the given text, using the contents of the full tweet status object for context.
    """
    for hashtag in tweet.entities.get('hashtags', []):
        text = text.replace('#' + hashtag['text'], hashtag['text'])

    for media in tweet.entities.get('media', []):
        text = text.replace(media['url'], '')

    for url in tweet.entities.get('urls', []):
        text = text.replace(url['url'], '')

    return text
