""" Twempest custom template filters unit tests.
"""

# This file is part of Twempest. Copyright 2017 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import datetime
import os
import pickle
import re

# noinspection PyPackageRequirements
import pytest

from twempest.filters import delink, isodate, reimage, relink, slugify


class MockContext:
    """ Stand-in for Jinja template context object.
    """
    def __init__(self, tweet):
        self.parent = {'tweet': tweet}


@pytest.fixture
def tweets():
    """ Just a whole mess--well, eleven--of pickled sample tweets from late 2016 to test with.
    """
    pickle_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "sample_tweets.p")
    return pickle.load(open(pickle_path, "rb"))


# noinspection PyShadowingNames
def test_delink(tweets):
    for tweet in tweets:
        delinked = delink(ctx=MockContext(tweet), text=tweet.text)

        for hashtag in tweet.entities.get('hashtags', []):
            assert '#' + hashtag['text'] not in delinked

        for media in tweet.entities.get('media', []):
            assert media['url'] not in delinked

        for url in tweet.entities.get('urls', []):
            assert url['url'] not in delinked

        # For good measure.
        assert "http://" not in delinked
        assert "https://" not in delinked


@pytest.mark.parametrize('date,expected', [
    (datetime.datetime(2017, 2, 14, 12, 44, 57, 557000), "2017-02-14"),
    (datetime.datetime(2016, 1, 1, 14, 23, 44, 590), "2016-01-01"),
    (datetime.date(2016, 2, 29), "2016-02-29"),
    (datetime.date(2016, 12, 31), "2016-12-31"),
])
def test_isodate(date, expected):
    assert isodate(date) == expected


# noinspection PyShadowingNames
def test_reimage(tweets):
    for tweet in tweets:
        reimaged = reimage(ctx=MockContext(tweet), text=tweet.text, tag_format="@@{{alt}}@@{{url}}@@")

        for media in tweet.entities.get('media', []):
            image_url = media['media_url_https'] if media['media_url_https'] else media['media_url']
            image_alt = os.path.splitext(os.path.basename(image_url))[0]

            if media['type'] == 'photo':
                assert media['url'] not in reimaged
                assert "@@{}@@{}@@".format(image_alt, image_url) in reimaged
            else:
                assert media['url'] in reimaged
                assert "@@{}@@{}@@".format(image_alt, image_url) not in reimaged

        for url in tweet.entities.get('urls', []):
            assert url['url'] in reimaged
            assert "@@{}@@{}@@".format(url['display_url'], url['expanded_url']) not in reimaged


# noinspection PyShadowingNames
def test_relink(tweets):
    for tweet in tweets:
        relinked = relink(ctx=MockContext(tweet), text=tweet.text, tag_format="@@{{text}}@@{{url}}@@")

        for hashtag in tweet.entities.get('hashtags', []):
            assert "@@#{}@@https://twitter.com/hashtag/{}@@".format(hashtag['text'], hashtag['text'].lower()) in relinked

        for media in tweet.entities.get('media', []):
            if media['type'] == 'photo':
                assert media['url'] in relinked
                assert "@@{}@@{}@@".format(media['display_url'], media['expanded_url']) not in relinked
            else:
                assert media['url'] not in relinked
                assert "@@{}@@{}@@".format(media['display_url'], media['expanded_url']) in relinked

        for url in tweet.entities.get('urls', []):
            assert url['url'] not in relinked
            assert "@@{}@@{}@@".format(url['display_url'], url['expanded_url']) in relinked


# noinspection PyShadowingNames
def test_slugify(tweets):
    only_allowed = re.compile(r"^[a-z0-9-]+$")

    for tweet in tweets:
        slugified = slugify(ctx=MockContext(tweet), text=tweet.text)
        assert only_allowed.match(slugified)
        assert "--" not in slugified
        assert not slugified.startswith('-')
        assert not slugified.endswith('-')
