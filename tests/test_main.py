""" Twempest console application unit tests.
"""

# This file is part of Twempest. Copyright 2017 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import os
import re

from click.testing import CliRunner

from twempest import __version__
from twempest.__main__ import choose_config_path, choose_option_values, choose_since_id, last_tweet_id_file_name,\
    CONFIG_FILE_NAME, CONFIG_OPTIONS, twempest


def test_choose_config_path():
    with CliRunner().isolated_filesystem():
        os.makedirs("fff/ggg/hhh")
        os.makedirs("iii/jjj")
        os.makedirs("kkk")

        root = os.getcwd()
        os.chdir("fff/ggg")
        possible_paths = [os.path.abspath(os.path.join(root, p)) for p in ["kkk", "iii/jjj", "fff/ggg"]]

        assert choose_config_path(possible_paths[0], possible_paths[1], possible_paths[2], CONFIG_FILE_NAME)[0] is None

        for i in [2, 1, 0]:
            with open(os.path.join(possible_paths[i], CONFIG_FILE_NAME), 'w') as f:
                f.write("[twitter]")

            assert (possible_paths[i], possible_paths) == choose_config_path(possible_paths[0], possible_paths[1], possible_paths[2],
                                                                             CONFIG_FILE_NAME)

        for i in [2, 1, 0]:
            os.chmod(possible_paths[i], 0o555)

        assert (None, possible_paths) == choose_config_path(possible_paths[0], possible_paths[1], possible_paths[2], CONFIG_FILE_NAME)


def test_choose_option_values():
    class MockConfig(dict):
        def getboolean(self, k, d):
            return bool(self.get(k, d))

    cli_options = {'replies': True}
    config = MockConfig()
    config['retweets'] = True
    options = choose_option_values(CONFIG_OPTIONS, cli_options, config)
    assert options['render-path'] == CONFIG_OPTIONS['render-path'].default
    assert options['replies'] is True
    assert options['retweets'] is True


def test_choose_since_id():
    with CliRunner().isolated_filesystem():
        user_id = "xxx"

        since_id = choose_since_id("1234", user_id, ".")
        assert since_id == "1234"

        with open(last_tweet_id_file_name(user_id), 'w') as f:
            f.write("6789")

        since_id = choose_since_id(None, user_id, ".")
        assert since_id == "6789"

        since_id = choose_since_id("1234", user_id, ".")
        assert since_id == "1234"


HELP_OPTION_REGEX = re.compile(r"^Usage: twempest.+Show this message and exit\.$")


def test_help_option_switch():
    def version_option_switch(option_switch):
        runner = CliRunner()
        result = runner.invoke(twempest, [option_switch])
        assert result.exit_code == 0
        print(result.output)
        match = HELP_OPTION_REGEX.match(result.output.replace("\n", ""))
        assert match is not None

    version_option_switch("-h")
    version_option_switch("--help")


def test_last_tweet_id_file_name():
    fn1 = last_tweet_id_file_name("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    fn2 = last_tweet_id_file_name("aaaaaaaaaaaaaaaaaaaaaaaaaaaaab")
    fn3 = last_tweet_id_file_name("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    assert fn1 == fn3
    assert fn1 != fn2


VERSION_OPTION_REGEX = re.compile(r"Twempest version (\d+\.\d+\.\d+)Copyright.+See LICENSE\.$")


def test_version_option_switch():
    def version_option_switch(option_switch):
        runner = CliRunner()
        result = runner.invoke(twempest, [option_switch])
        assert result.exit_code == 0
        match = VERSION_OPTION_REGEX.match(result.output.replace("\n", ""))
        assert match.group(1) == __version__

    version_option_switch("-V")
    version_option_switch("--version")
