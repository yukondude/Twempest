""" Twempest rendering logic.
"""

# This file is part of Twempest. Copyright 2017 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import os
import pickle
import urllib.request as request

import jinja2
import pytz
import tweepy
import tzlocal

from .filters import ALL_FILTERS


PICKLE_FILE_NAME = "twempest.p"


class TwempestError(Exception):
    pass


def authenticate_twitter_api(consumer_key, consumer_secret, access_token, access_token_secret):
    """ Return the Twitter API object for the given authentication credentials.
    """
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)


def cleanup_downloaded_images(downloaded_image_file_paths, echo):
    """ Clean up any downloaded images for the skipped tweet. Clunky, but simpler than avoiding downloading in the first place. Warn of any
        image files that couldn't be deleted using the passed echo() function but continue on regardless.
    """
    for path in downloaded_image_file_paths:
        try:
            os.unlink(path)
        except OSError as e:
            echo("Warning: Unable to delete downloaded image file: {}".format(e), err=True)


def download_from_url(url, file_path):
    """ Download the file at the given url and store it at the given file path. Raise a TwempestError exception if anything goes wrong.
    """
    try:
        request.urlretrieve(url, file_path)
    except request.URLError as e:
        raise TwempestError("Unable to download image file: {}".format(e))
    except OSError as e:
        raise TwempestError("Unable to write downloaded image file: {}".format(e))


def download_images(tweet, image_dir_path_template, image_url_path_template, render_file_name, download_func, echo):
    """ Download any images for the given tweet, storing them in the rendered image directory path template and updating their URLs with the
        rendered image URL path template. Echo any skipped images that already exist to the console using the passed echo() function. Return
        the list of file paths for the downloaded images.
    """
    downloaded_image_file_paths = []
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
        media['original_media_url_https'] = media['media_url_https']
        media['media_url_https'] = image_url_path if is_https else None
        media['original_media_url'] = media['media_url']
        media['media_url'] = image_url_path if not is_https else None

        if os.path.exists(image_file_path):
            echo("Warning: Skipping existing image file '{}'.".format(image_file_path), err=True)
            continue

        download_func(image_download_url, image_file_path)
        downloaded_image_file_paths.append(image_file_path)

    return downloaded_image_file_paths


def render(tweets, options, template_text, download_func, echo):
    """ Render the given tweets using the supplied template text. Also download images if requested. Write any warning messages to the
        console using the passed echo() function, and raise all errors as TwempestError.
    """
    def write_to_console(text):
        """ Write the given text to the console with a following blank line.
        """
        echo(text)
        echo()

    def write_to_file(path):
        """ Return a function that will write text to a file at the given path.
        """
        def write_to_file_inner(text):
            """ Write the given text to the outer function's file path.
            """
            try:
                with open(path, 'a') as f:
                    f.write(text)
            except OSError as oe:
                raise TwempestError("Unable to write rendered tweet: {}".format(oe))

        return write_to_file_inner

    # noinspection PyUnusedLocal
    def write_to_void(text):
        """ Don't do anything with the given text.
        """
        pass

    env = jinja2.Environment()
    env.filters.update(ALL_FILTERS)
    template = env.from_string(template_text)

    image_dir_path_template = env.from_string(options['image-path']) if options['image-path'] else None
    image_url_path_template = env.from_string(options['image-url']) if options['image-url'] else None
    render_file_name_template = env.from_string(options['render-file']) if options['render-file'] else None
    render_dir_path_template = env.from_string(options['render-path'])

    gmt_tz = pytz.timezone('UTC')
    local_tz = tzlocal.get_localzone()

    count_remaining = options['count']
    last_tweet_id = None
    pickle_tweets = []

    for tweet in tweets:
        # Replace UTC created time with local time.
        if tweet.created_at.tzinfo is None:
            tweet.created_at = gmt_tz.localize(tweet.created_at)

        tweet.created_at = tweet.created_at.astimezone(local_tz)

        if not options['replies'] and tweet.in_reply_to_status_id and tweet.text[0] == '@':
            continue

        if render_file_name_template:
            render_dir_path = os.path.abspath(render_dir_path_template.render(tweet=tweet))
            os.makedirs(render_dir_path, exist_ok=True)
            render_file_name = render_file_name_template.render(tweet=tweet)
            render_file_path = os.path.join(render_dir_path, render_file_name)
            downloaded_image_file_paths = download_images(tweet, image_dir_path_template, image_url_path_template, render_file_name,
                                                          download_func, echo) if options['image-path'] else []

            if not options['append'] and os.path.exists(render_file_path):
                echo("Warning: Skipping existing file '{}'. Use --append to append rendered tweets instead.".format(render_file_path),
                     err=True)
                write_func = write_to_void
            else:
                write_func = write_to_file(render_file_path)
        else:
            downloaded_image_file_paths = []
            write_func = write_to_console

        rendered_tweet = template.render(tweet=tweet)

        if options['skip'] and options['skip'].search(rendered_tweet) is not None:
            echo("Warning: Skipping tweet ID {} ('{}{}') because its rendered form matches the --skip pattern."
                 .format(tweet.id, tweet.text[:30], "..." if len(tweet.text) > 30 else ""), err=True)
            cleanup_downloaded_images(downloaded_image_file_paths, echo)
            continue

        write_func(rendered_tweet)
        last_tweet_id = tweet.id

        # Check the count here as the list has already been "filtered" by this point and so the count remaining reflects the actual number
        # of tweets left to render.
        count_remaining -= 1
        pickle_tweets.append(tweet)

        if count_remaining == 0:
            break

    if not last_tweet_id:
        echo("Warning: No tweets were retrieved.", err=True)
    elif options['pickle']:
        try:
            with open(PICKLE_FILE_NAME, "wb") as pf:
                pickle.dump(pickle_tweets, pf)
        except OSError as e:
            echo("Warning: Unable to serialize the rendered tweets to '{}' in the current working directory: {}".format(PICKLE_FILE_NAME,
                                                                                                                        e))

    return last_tweet_id


def retrieve(auth_keys, options, template_text, echo):
    """ Using the given authorization credentials and rendering options, retrieve and render the tweets from the authorized user's timeline.
    """
    api = authenticate_twitter_api(**auth_keys)

    try:
        tweets = reversed(list(tweepy.Cursor(api.user_timeline, since_id=options['since-id'], include_rts=options['retweets']).items()))
    except tweepy.TweepError as e:
        raise TwempestError("Unable to retrieve tweets. Twitter API responded with '{}'. "
                            "See https://dev.twitter.com/overview/api/response-codes for an explanation.".format(e.response))

    return render(tweets, options, template_text, download_from_url, echo)
