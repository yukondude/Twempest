""" Twempest console script entry point.
"""

# This file is part of Twempest. Copyright 2017 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import configparser
import os

import click
import tweepy


CONFIG_FILE_NAME = "twempest.conf"
DEFAULT_CONFIG_PATH = "~/.twempest/"


def choose_config_path(cli_config_path):
    """ Choose the most likely configuration path from, in order: the given path, the default path, and the path of this module. To be
        valid, the config path must contain a twempest.conf file.
    """
    here = os.path.dirname(os.path.realpath(__file__))
    abs_cli_config_path = os.path.abspath(os.path.expanduser(cli_config_path))

    for possible_path in (abs_cli_config_path, DEFAULT_CONFIG_PATH, here):
        if os.path.isfile(os.path.join(possible_path, CONFIG_FILE_NAME)):
            return possible_path

    raise click.ClickException("Could not find twempest.conf file in config path '{}' or alternate locations.".format(abs_cli_config_path))


# noinspection PyUnusedLocal
def show_version(ctx, param, value):
    """ Display the version message.
    """
    if not value or ctx.resilient_parsing:
        return  # pragma: no cover
    from twempest import __version__
    click.echo("Twempest version {}".format(__version__))
    click.echo("Copyright 2017 Dave Rogers. Licensed under the GPLv3. See LICENSE.")
    ctx.exit()


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option("--config-path", "-c", default=DEFAULT_CONFIG_PATH, show_default=True,
              help="Twempest configuration directory path. The twempest.conf file must exist in this location.")
@click.option("--replies", "-@", is_flag=True, default=False, help="Include @replies in the list of retrieved tweets.")
@click.option("--retweets", "-r", is_flag=True, default=False, help="Include retweets in the list of retrieved tweets.")
@click.option("--version", "-V", is_flag=True, callback=show_version, expose_value=False, is_eager=True, help="Show version and exit.")
def twempest(config_path, replies, retweets):
    """ Download a sequence of recent Twitter tweets and convert these, via template, to text format.
    """
    config = configparser.ConfigParser()
    config_path = choose_config_path(config_path)
    config.read(os.path.join(config_path, CONFIG_FILE_NAME))
    twitter_config = config['twitter']

    auth = tweepy.OAuthHandler(twitter_config['consumer_key'], twitter_config['consumer_secret'])
    auth.set_access_token(twitter_config['access_token'], twitter_config['access_token_secret'])
    api = tweepy.API(auth)

    public_tweets = api.user_timeline(count=50, include_rts=retweets)

    for tweet in public_tweets:
        try:
            if not replies and tweet.in_reply_to_status_id:
                continue

            print(tweet.id, tweet.created_at, tweet.text)
        except AttributeError:
            print(tweet.id, "NOPE")
