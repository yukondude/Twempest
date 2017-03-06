""" Twempest console script entry point.
"""

# This file is part of Twempest. Copyright 2017 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import collections
import configparser
import hashlib
import os
import re

import click

from .twempest import render, TwempestError


# Global config 'constants'.
CONFIG_FILE_NAME = "twempest.config"
DEFAULT_CONFIG_DIR_PATH = "~/.twempest"
FALLBACK_CONFIG_DIR_PATH = "."

# Collect all configuration options (that may also appear in the config file) here so that they don't have to be duplicated.
ConfigOption = collections.namedtuple('ConfigOption', "short default show_default is_flag help")
CONFIG_OPTIONS = {
    'append': ConfigOption(short='a', default=False, show_default=False, is_flag=True,
                           help="Append rendered tweet(s) to existing file(s) rather than skipping past with a warning."),
    'dry-run': ConfigOption('D', False, False, True, "Display all configuration options and template contents without retrieving tweets."),
    'image-path': ConfigOption('i', None, False, False, "The directory path (template tags allowed) to write downloaded image "
                                                        "(media type == 'photo') files. "
                                                        "The directory path will be created if it doesn't exist. "
                                                        "Media file names use the --render-file name followed by a number and the "
                                                        "appropriate file extension. "
                                                        "If omitted, media files will not be downloaded."),
    'image-url': ConfigOption('u', None, False, False, "The URL path (template tags allowed) to use for all image files downloaded via the "
                                                       "--image-path option."),
    'render-file': ConfigOption('f', None, False, False, "The file name (template tags allowed) for the rendered tweets. "
                                                         "If omitted, tweets will be rendered to STDOUT."),
    'render-path': ConfigOption('p', ".", True, False, "The directory path (template tags allowed) to write the rendered tweet files. "
                                                       "The directory path will be created if it doesn't exist."),
    'replies': ConfigOption('@', False, False, True, "Include @replies in the list of retrieved tweets."),
    'retweets': ConfigOption('r', False, False, True, "Include retweets in the list of retrieved tweets."),
    'since-id': ConfigOption('s', None, False, False, "Retrieve tweets that follow this ID in the timeline. "
                                                      "Required, unless the ID has already been recorded in the config path directory "
                                                      "after a previous run of Twempest."),
    'skip': ConfigOption('k', None, False, False, "Skip any rendered tweets that contain this regular expression pattern."),
}


def choose_config_path(cli_dir_path, default_dir_path, fallback_dir_path, file_name):
    """ Choose the most likely configuration path from, in order: the CLI config-path option, the default path, and the fallback path
        (current directory). To be valid, the config path must contain a twempest.conf file and the directory must be writable. Return
        both the chosen path and the possible paths as a tuple.
    """
    # Using keys of OrderedDict simulates an OrderedSet type.
    unique_paths = collections.OrderedDict([(os.path.abspath(os.path.expanduser(p)), None) for p in (cli_dir_path, default_dir_path,
                                                                                                     fallback_dir_path)])
    possible_paths = list(unique_paths.keys())

    for possible_path in possible_paths:
        possible_config_path = os.path.join(possible_path, file_name)

        if os.path.isfile(possible_config_path) and os.access(possible_config_path, os.R_OK) and os.access(possible_path, os.W_OK):
            return possible_path, possible_paths

    return None, possible_paths


def choose_option_values(config_options, cli_options, config):
    """ For each of the options given, choose a value from, in order: the CLI option, the config file, the CONFIG_OPTIONS default. Return
        the option values in a tuple.
    """
    options = {}

    for option, config_option in config_options.items():
        cli_option = option.replace('-', '_')
        config_func = config.getboolean if config_option.is_flag else config.get

        if (config_option.is_flag and not cli_options.get(cli_option, False)) or cli_options.get(cli_option) is None:
            # Ignore False CLI flags or unset CLI options so that they don't mask config file or option defaults.
            options[option] = config_func(option, config_option.default)
        else:
            options[option] = cli_options.get(cli_option)

    return options


def choose_since_id(cli_since_id, user_id, config_dir_path):
    """ Choose the most likely since ID value from, in order: the CLI since-id option, and a record of the ID written to a file in the
        config directory using the given user_id to distinguish it from others.
    """
    since_id = cli_since_id

    if since_id:
        return since_id

    # Hash the user ID so that it's unique to that user, but doesn't reveal part of the authentication credentials in the file name.
    last_id_file_name = last_tweet_id_file_name(user_id)
    last_id_file_path = os.path.join(config_dir_path, last_id_file_name)

    if os.path.isfile(last_id_file_path):
        with open(last_id_file_path, 'r') as f:
            since_id = f.read()

    return since_id


def decorate_config_options(options):
    """ Return a decorator with all of the CONFIG_OPTIONS items as a chain of click.option decorators, sorted by option name.
    """
    def option_decorators(fn):
        """ Return the decorator chain wrapped around the given function.
        """
        decorators = fn

        for option, config_option in sorted(options.items(), reverse=True):
            help_text = config_option.help

            if config_option.show_default:
                help_text += "  [default: {}]".format(config_option.default)

            # Don't specify a default value for the option, as it will be the fallback when choose_option_values() is called. For this
            # reason, append the default to the help text manually if it is to be shown.
            decorator = click.option("--" + option, "-" + config_option.short, is_flag=config_option.is_flag, help=help_text)
            decorators = decorator(decorators)

        return decorators

    return option_decorators


def last_tweet_id_file_name(user_id):
    """ Return the last tweet ID file name corresponding to the given user.
    """
    return "twempest-last-{}.id".format(hashlib.sha1(user_id.encode('utf-8')).hexdigest())


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
@click.option("--config-path", "-c", default=DEFAULT_CONFIG_DIR_PATH, show_default=True,
              help="Twempest configuration directory path, which must be writable, and must also contain the twempest.conf file.")
@decorate_config_options(CONFIG_OPTIONS)
@click.option("--version", "-V", is_flag=True, callback=show_version, expose_value=False, is_eager=True, help="Show version and exit.")
@click.argument("template", type=click.File('r'))
def twempest(**kwargs):
    """ Download a sequence of recent Twitter tweets and convert these, via the given template file, to text format.
        Twempest uses the Jinja template syntax throughout: http://jinja.pocoo.org/docs/2.9/templates/
    """
    config = configparser.RawConfigParser(allow_no_value=True)
    config_dir_path, possible_paths = choose_config_path(cli_dir_path=kwargs['config_path'], default_dir_path=DEFAULT_CONFIG_DIR_PATH,
                                                         fallback_dir_path=FALLBACK_CONFIG_DIR_PATH, file_name=CONFIG_FILE_NAME)

    if not config_dir_path:
        raise click.ClickException("Could not find readable twempest.conf configuration file in writable directory path(s): '{}'"
                                   .format("', '".join(possible_paths)))

    config_file_path = os.path.join(config_dir_path, CONFIG_FILE_NAME)
    config.read(config_file_path)

    try:
        twitter_config = config['twitter']
        twempest_config = config['twempest']
    except KeyError as e:
        raise click.ClickException("Could not find required '[{}]' section in '{}'".format(str(e).strip("'"), config_file_path))

    try:
        auth_keys = {k: twitter_config[k] for k in ('consumer_key', 'consumer_secret', 'access_token', 'access_token_secret')}
    except KeyError as e:
        raise click.ClickException("Could not find required Twitter authentication credential {} in '{}'".format(str(e), config_file_path))

    options = choose_option_values(config_options=CONFIG_OPTIONS, cli_options=kwargs, config=twempest_config)
    options['config-path'] = config_file_path

    if options['image-path'] and not options['render-file']:
        raise click.ClickException("Cannot download images unless the --render-file option is also specified.")

    if options['image-url'] and not options['image-path']:
        raise click.ClickException("The --image-url option may only be specified if the --image-path option is as well.")

    options['since-id'] = choose_since_id(cli_since_id=options['since-id'], user_id=twitter_config['consumer_key'],
                                          config_dir_path=config_dir_path)

    if not options['since-id']:
        raise click.ClickException("The --since-id option is required since the ID was not recorded in '{}' after a previous run of "
                                   "Twempest. To find the ID, open a specific tweet on the Twitter website and view the page's address: "
                                   "the long number following 'status/' is that tweet's ID."
                                   .format(config_dir_path))

    if options['skip'] is not None:
        try:
            # Replace skip option with compiled regular expression.
            options['skip'] = re.compile(options['skip'])
        except re.error as e:
            raise click.ClickException("Syntax problem with --skip regular expression: {}".format(e))

    template_file = kwargs['template']

    try:
        template_text = template_file.read()
    except OSError as e:
        raise click.ClickException("Unable to read template file: {}".format(e))

    if options['dry-run']:
        for option in sorted(options.keys()):
            click.echo("{} = {}".format(option, options[option]))

        click.echo()
        click.echo("template =")
        click.echo(template_text)
    else:
        try:
            last_tweet_id = render(auth_keys=auth_keys, options=options, template_text=template_text, echo=click.echo)
        except TwempestError as e:
            raise click.ClickException(e)

        if last_tweet_id:
            with open(os.path.join(config_dir_path, last_tweet_id_file_name(user_id=twitter_config['consumer_key'])), 'w') as f:
                try:
                    f.write(str(last_tweet_id))
                except OSError as e:
                    raise click.ClickException("Unable to write last tweet ID file: {}".format(e))
