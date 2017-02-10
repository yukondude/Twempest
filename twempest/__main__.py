""" Twempest console script entry point.
"""

# This file is part of Twempest. Copyright 2017 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import configparser
import os

import click
import tweepy


# noinspection PyUnusedLocal
def show_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return  # pragma: no cover
    from twempest import __version__
    click.echo("Twempest version {}".format(__version__))
    click.echo("Copyright 2017 Dave Rogers. Licensed under the GPLv3. See LICENSE.")
    ctx.exit()


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option("--version", "-V", is_flag=True, callback=show_version, expose_value=False, is_eager=True, help="Show version and exit.")
def twempest():
    """ Download a sequence of recent Twitter tweets and convert these, via template, to text format.
    """
    here = os.path.dirname(os.path.realpath(__file__))

    config = configparser.ConfigParser()
    config.read(os.path.join(here, "twempest.conf"))
    twitter_config = config['twitter']

    auth = tweepy.OAuthHandler(twitter_config['consumer_key'], twitter_config['consumer_secret'])
    auth.set_access_token(twitter_config['access_token'], twitter_config['access_token_secret'])
    api = tweepy.API(auth)

    public_tweets = api.user_timeline(include_rts=True)

    for tweet in public_tweets[:10]:
        try:
            print(tweet.id, tweet.created_at, tweet.text)
        except AttributeError:
            print(tweet.id, "NOPE")
