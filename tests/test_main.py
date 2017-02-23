""" Twempest console application unit tests.
"""

# This file is part of Twempest. Copyright 2017 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import re

from click.testing import CliRunner

from twempest import __version__
from twempest.__main__ import twempest


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
