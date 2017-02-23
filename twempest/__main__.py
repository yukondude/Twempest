""" Twempest console script entry point.
"""

# This file is part of Twempest. Copyright 2017 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import collections
import configparser
import os

import click
import jinja2
import tweepy

from twempest.filters import ALL_FILTERS


CONFIG_FILE_NAME = "twempest.config"
DEFAULT_CONFIG_PATH = "~/.twempest"

# Collect all configuration options (that may also appear in the config file) here so that they don't have to be duplicated.
ConfigOption = collections.namedtuple('ConfigOption', "short default show_default is_flag help")
CONFIG_OPTIONS = {
    'render-file': ConfigOption(short='f', default=None, show_default=False, is_flag=False,
                                help="The file name (template tags allowed) for the rendered tweets. "
                                     "If the file already exists, the rendered tweet will be appended to it. "
                                     "If omitted, tweets will be rendered to STDOUT."),
    'render-path': ConfigOption('p', ".", True, False, "The directory path (template tags allowed) to write the rendered tweet files. "
                                                       "The directory path will be created if it doesn't exist."),
    'replies': ConfigOption('@', False, False, True, "Include @replies in the list of retrieved tweets."),
    'retweets': ConfigOption('r', False, False, True, "Include retweets in the list of retrieved tweets."),
    'since-id': ConfigOption('s', None, False, False, "Retrieve tweets that follow this ID in the timeline. "
                                                      "Required, unless the ID has already been recorded in the config path directory "
                                                      "after a previous run of Twempest."),
}


def authenticate_twitter_api(consumer_key, consumer_secret, access_token, access_token_secret):
    """ Return the Twitter API object for the given authentication credentials.
    """
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)


def choose_config_path(cli_config_path):
    """ Choose the most likely configuration path from, in order: the given path, the default path, and the current working directory. To be
        valid, the config path must contain a twempest.conf file and the directory must be writable.
    """
    # Using keys of OrderedDict simulates an OrderedSet type.
    possible_paths = collections.OrderedDict([(os.path.abspath(os.path.expanduser(p)), None) for p in (cli_config_path,
                                                                                                       DEFAULT_CONFIG_PATH,
                                                                                                       ".")])

    for possible_path in possible_paths:
        possible_config_path = os.path.join(possible_path, CONFIG_FILE_NAME)

        if os.path.isfile(possible_config_path) and os.access(possible_config_path, os.R_OK) and os.access(possible_path, os.W_OK):
            return possible_path

    raise click.ClickException("Could not find readable twempest.conf configuration file in writable directory path(s): '{}'"
                               .format("', '".join(possible_paths.keys())))


def choose_option_values(options, cli_args, config):
    """ For each of the options given, choose a value from, in order: the CLI switch option, the config file, the CONFIG_OPTIONS default.
        Return the option values in a tuple.
    """
    option_values = {}

    for option, config_option in options.items():
        option_arg = option.replace('-', '_')
        config_func = config.getboolean if config_option.is_flag else config.get

        if config_option.is_flag and not cli_args.get(option_arg, False):
            # Ignore false CLI flags so that they don't mask config file or option defaults.
            option_values[option] = config_func(option, config_option.default)
        elif cli_args.get(option_arg) is None:
            option_values[option] = config_func(option, config_option.default)
        else:
            option_values[option] = cli_args.get(option_arg, config_func(option, config_option.default))

    return option_values


def config_options(fn):
    """ Return a decorator with all of the CONFIG_OPTIONS items as a chain of click.option decorators, sorted in ascending order by option
        name.
    """
    def option_decorators(inner_fn):
        """ Return the decorator chain wrapped around the given function.
        """
        decorators = inner_fn

        for option, config_option in sorted(CONFIG_OPTIONS.items(), reverse=True):
            decorator = click.option("--" + option, "-" + config_option.short, default=config_option.default,
                                     show_default=config_option.show_default, is_flag=config_option.is_flag, help=config_option.help)
            decorators = decorator(decorators)

        return decorators

    return option_decorators(fn)


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
@config_options
@click.option("--version", "-V", is_flag=True, callback=show_version, expose_value=False, is_eager=True, help="Show version and exit.")
@click.argument("template", type=click.File('r'))
def twempest(**kwargs):
    """ Download a sequence of recent Twitter tweets and convert these, via the given template file, to text format.
        Twempest uses the Jinja template syntax throughout: http://jinja.pocoo.org/docs/2.9/templates/
    """
    config = configparser.RawConfigParser(allow_no_value=True)
    config_dir_path = choose_config_path(kwargs['config_path'])
    config_file_path = os.path.join(config_dir_path, CONFIG_FILE_NAME)
    config.read(config_file_path)

    try:
        twitter_config = config['twitter']
        twempest_config = config['twempest']
    except KeyError as e:
        raise click.ClickException("Could not find required '[{}]' section in '{}'".format(str(e).strip("'"), config_file_path))

    try:
        auth_keys = {k: twitter_config[k] for k in ('consumer_key', 'consumer_secret', 'access_token', 'access_token_secret')}
        api = authenticate_twitter_api(**auth_keys)
    except KeyError as e:
        raise click.ClickException("Could not find required Twitter authentication credential {} in '{}'".format(str(e), config_file_path))

    option_values = choose_option_values(options=CONFIG_OPTIONS, cli_args=kwargs, config=twempest_config)

    if not option_values['since-id']:
        # TODO: Load since_id from config directory if possible
        raise click.ClickException("--since-id option is required since the ID was not recorded in '{}' after a previous run of Twempest."
                                   .format(config_dir_path))

    env = jinja2.Environment()
    env.filters.update(ALL_FILTERS)
    template = env.from_string(kwargs['template'].read())

    render_file_template = env.from_string(option_values['render-file']) if option_values['render-file'] else None
    render_path_template = env.from_string(option_values['render-path'])

    try:
        tweets = list(tweepy.Cursor(api.user_timeline, since_id=option_values['since-id'],
                                    include_rts=option_values['retweets']).items())
    except tweepy.TweepError as e:
        raise click.ClickException(e)

    i = 0

    for tweet in reversed(tweets):
        try:
            if not option_values['replies'] and tweet.in_reply_to_status_id and tweet.text[0] == '@':
                continue

            print(template.render(tweet=tweet))
            print()
            print(render_path_template.render(tweet=tweet))

            if render_file_template:
                print(render_file_template.render(tweet=tweet))

            print()
        except AttributeError as e:
            print(tweet.id, "NOPE", str(e))

        i += 1

        if i > 10:
            break
