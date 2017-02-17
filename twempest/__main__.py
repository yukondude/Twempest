""" Twempest console script entry point.
"""

# This file is part of Twempest. Copyright 2017 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import collections
import configparser
import os

import click
import tweepy


CONFIG_FILE_NAME = "twempest.conf"
DEFAULT_CONFIG_PATH = "~/.twempest"

ConfigOption = collections.namedtuple('ConfigOption', "setting default")

CONFIG_OPTIONS = {
    'replies': ConfigOption(setting='replies', default=False),
    'retweets': ConfigOption('retweets', False),
    'template': ConfigOption('template', None),
}


def choose_config_path(cli_config_path):
    """ Choose the most likely configuration path from, in order: the given path, the default path, and the path of this module. To be
        valid, the config path must contain a twempest.conf file and the directory must be writable.
    """
    # Using keys of OrderedDict simulates an OrderedSet type.
    possible_paths = collections.OrderedDict([(os.path.abspath(os.path.expanduser(p)), None)
                                              for p in (cli_config_path, DEFAULT_CONFIG_PATH, os.path.dirname(os.path.realpath(__file__)))])

    for possible_path in possible_paths:
        possible_config_path = os.path.join(possible_path, CONFIG_FILE_NAME)

        if os.path.isfile(possible_config_path) and os.access(possible_config_path, os.R_OK) and os.access(possible_path, os.W_OK):
            return possible_path

    raise click.ClickException("Could not find readable twempest.conf configuration file in writable directory path(s): '{}'"
                               .format("', '".join(possible_paths.keys())))


def choose_config_setting(setting, options, config, is_flag=False):
    """ Choose the configuration setting from, in order: the CLI switch option, the config file, the CONFIG_OPTIONS default.
    """
    config_func = config.getboolean if is_flag else config.get

    if is_flag and not options.get(setting, False):
        # Ignore false CLI flags so that they don't mask config file or option defaults.
        return config_func(CONFIG_OPTIONS[setting].setting, CONFIG_OPTIONS[setting].default)

    return options.get(setting, config_func(CONFIG_OPTIONS[setting].setting, CONFIG_OPTIONS[setting].default))


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
@click.option("--" + CONFIG_OPTIONS['replies'].setting, "-@", is_flag=True, help="Include @replies in the list of retrieved tweets.")
@click.option("--" + CONFIG_OPTIONS['retweets'].setting, "-r", is_flag=True, help="Include retweets in the list of retrieved tweets.")
@click.option("--version", "-V", is_flag=True, callback=show_version, expose_value=False, is_eager=True, help="Show version and exit.")
def twempest(**kwargs):
    """ Download a sequence of recent Twitter tweets and convert these, via template, to text format.
    """
    config = configparser.ConfigParser()
    config_path = choose_config_path(kwargs['config_path'])
    config.read(os.path.join(config_path, CONFIG_FILE_NAME))

    twitter_config = config['twitter']
    auth = tweepy.OAuthHandler(twitter_config['consumer_key'], twitter_config['consumer_secret'])
    auth.set_access_token(twitter_config['access_token'], twitter_config['access_token_secret'])
    api = tweepy.API(auth)

    twempest_config = config['twempest']
    include_replies = choose_config_setting(setting='replies', options=kwargs, config=twempest_config, is_flag=True)
    include_retweets = choose_config_setting('retweets', kwargs, twempest_config, True)

    tweets = list(tweepy.Cursor(api.user_timeline, since_id="804358482535149569", include_rts=include_retweets).items())

    for tweet in reversed(tweets):
        try:
            if not include_replies and tweet.in_reply_to_status_id and tweet.text[0] == '@':
                continue

            print(tweet.id, tweet.created_at, tweet.text)
        except AttributeError:
            print(tweet.id, "NOPE")
