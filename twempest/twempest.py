""" Twempest rendering logic.
"""

# This file is part of Twempest. Copyright 2017 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import jinja2
import os
import pytz
import tweepy
import tzlocal
import urllib.request as request

from .filters import ALL_FILTERS


class TwempestError(Exception):
    pass


def authenticate_twitter_api(consumer_key, consumer_secret, access_token, access_token_secret):
    """ Return the Twitter API object for the given authentication credentials.
    """
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)


def render(auth_keys, options, template_text, echo):
    """ Using the given authorization credentials and rendering options, retrieve the tweets from the authorized user's timeline and render
        them using the given template text. Also download images if requested. Write any warning messages to the console using the passed
        echo() function, and raise all errors as TwempestError.
    """
    env = jinja2.Environment()
    env.filters.update(ALL_FILTERS)
    template = env.from_string(template_text)

    image_dir_path_template = env.from_string(options['image-path']) if options['image-path'] else None
    image_url_path_template = env.from_string(options['image-url']) if options['image-url'] else None
    render_file_name_template = env.from_string(options['render-file']) if options['render-file'] else None
    render_dir_path_template = env.from_string(options['render-path'])

    api = authenticate_twitter_api(**auth_keys)

    gmt_tz = pytz.timezone('UTC')
    local_tz = tzlocal.get_localzone()

    last_tweet_id = None

    try:
        tweets = list(tweepy.Cursor(api.user_timeline, since_id=options['since-id'], include_rts=options['retweets']).items())
    except tweepy.TweepError as e:
        raise TwempestError("Unable to retrieve tweets. Twitter API responded with '{}'. "
                            "See https://dev.twitter.com/overview/api/response-codes for an explanation.".format(e.response))

    for tweet in reversed(tweets):
        # Replace UTC created time with local time.
        tweet.created_at = gmt_tz.localize(tweet.created_at).astimezone(local_tz)

        if not options['replies'] and tweet.in_reply_to_status_id and tweet.text[0] == '@':
            continue

        if render_file_name_template:
            render_dir_path = os.path.abspath(render_dir_path_template.render(tweet=tweet))
            os.makedirs(render_dir_path, exist_ok=True)
            render_file_name = render_file_name_template.render(tweet=tweet)
            render_file_path = os.path.join(render_dir_path, render_file_name)
            downloaded_image_file_paths = []

            if options['image-path']:
                image_dir_path = os.path.abspath(image_dir_path_template.render(tweet=tweet))
                os.makedirs(image_dir_path, exist_ok=True)

                for i, media in enumerate(m for m in tweet.entities.get('media', []) if m['type'] == 'photo'):
                    image_download_url = media['media_url_https'] if media['media_url_https'] else media['media_url']
                    image_file_name = "{}-{}{}".format(os.path.splitext(render_file_name)[0], i,
                                                       os.path.splitext(os.path.basename(image_download_url))[1])
                    image_file_path = os.path.join(image_dir_path, image_file_name)
                    image_url_path = image_url_path_template.render(tweet=tweet).rstrip('/') + '/' + image_file_name

                    # Inject the downloaded image URL into the tweet status object and backup the original media URL(s) just in case.
                    is_https = image_url_path.lower().startswith("https")
                    media['media_url_https'] = image_url_path if is_https else None
                    media['original_media_url_https'] = media['media_url_https']
                    media['media_url'] = image_url_path if not is_https else None
                    media['original_media_url'] = media['media_url']

                    if os.path.exists(image_file_path):
                        echo("Warning: Skipping existing image file '{}'.".format(image_file_path), err=True)
                        continue

                    try:
                        request.urlretrieve(image_download_url, image_file_path)
                        downloaded_image_file_paths.append(image_file_path)
                    except request.URLError as e:
                        raise TwempestError("Unable to download image file: {}".format(e))
                    except OSError as e:
                        raise TwempestError("Unable to write downloaded image file: {}".format(e))

            if not options['append'] and os.path.exists(render_file_path):
                echo("Warning: Skipping existing file '{}'. Use --append to append rendered tweets instead.".format(render_file_path),
                     err=True)
                continue

            rendered_tweet = template.render(tweet=tweet)

            if options['skip'] and options['skip'].search(rendered_tweet) is not None:
                echo("Warning: Skipping tweet ID {} ('{}{}') because its rendered form matches the --skip pattern."
                     .format(tweet.id, tweet.text[:30], "..." if len(tweet.text) > 30 else ""), err=True)

                # Clean up any downloaded images for the skipped tweet. Clunky, but simpler than avoiding downloading in the first place.
                for path in downloaded_image_file_paths:
                    try:
                        os.unlink(path)
                    except OSError as e:
                        echo("Warning: Unable to delete downloaded image file: {}".format(e), err=True)

                continue

            try:
                with open(render_file_path, 'a') as f:
                    f.write(rendered_tweet)
            except OSError as e:
                raise TwempestError("Unable to write rendered tweet: {}".format(e))
        else:
            echo(template.render(tweet=tweet))
            echo()

        last_tweet_id = tweet.id

    if not last_tweet_id:
        echo("Warning: No tweets were retrieved.", err=True)

    return last_tweet_id
