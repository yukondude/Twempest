""" Twempest rendering logic.
"""

# This file is part of Twempest. Copyright 2017 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import jinja2
import pytz
import tweepy
import tzlocal

from twempest.filters import ALL_FILTERS


class TwempestException(Exception):
    pass


def authenticate_twitter_api(consumer_key, consumer_secret, access_token, access_token_secret):
    """ Return the Twitter API object for the given authentication credentials.
    """
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)


def render(auth_keys, options, template_text):
    env = jinja2.Environment()
    env.filters.update(ALL_FILTERS)
    template = env.from_string(template_text)

    render_file_template = env.from_string(options['render-file']) if options['render-file'] else None
    render_path_template = env.from_string(options['render-path'])

    api = authenticate_twitter_api(**auth_keys)

    gmt_tz = pytz.timezone('UTC')
    local_tz = tzlocal.get_localzone()

    try:
        tweets = list(tweepy.Cursor(api.user_timeline, since_id=options['since-id'], include_rts=options['retweets']).items())[-14:]
    except tweepy.TweepError as e:
        raise TwempestException("Unable to retrieve tweets. Twitter API responded with '{}'. "
                                "See https://dev.twitter.com/overview/api/response-codes for an explanation.".format(e.response))

    for tweet in reversed(tweets):
        # Replace UTC created time with local time.
        tweet.created_at = gmt_tz.localize(tweet.created_at).astimezone(local_tz)

        if not options['replies'] and tweet.in_reply_to_status_id and tweet.text[0] == '@':
            continue

        print(template.render(tweet=tweet))
        print()
        print(render_path_template.render(tweet=tweet))

        if render_file_template:
            print(render_file_template.render(tweet=tweet))

        print()
