#!/usr/bin/env python
""" (Re)build the README.md file from README-template.md.
"""

# This file is part of Twempest. Copyright 2017 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import datetime
import os
import subprocess

import twempest


if __name__ == '__main__':
    here = os.path.abspath(os.path.dirname(__file__))

    with open(os.path.join(here, "README-template.md"), "r") as f:
        readme = f.read()

    today = datetime.date.today().strftime("%B %-d, %Y")
    version = twempest.__version__

    readme = readme.replace("@@TODAY@@", today)
    readme = readme.replace("@@VERSION@@", version)

    help_text = subprocess.check_output(["twempest", "--help"]).decode("utf-8").strip()
    readme = readme.replace("@@HELPTEXT@@", help_text)

    with open(os.path.join(here, "README.md"), "w") as f:
        f.write(readme)
