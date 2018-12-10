#!/usr/bin/env python
""" Re-build the given homebrew formula from STDIN and output it to STDOUT.
"""

# This file is part of Twempest. Copyright 2018 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public
# License, version 3. Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import sys
import twempest


if __name__ == '__main__':
    description = " ".join(twempest.__doc__.strip().split()).replace('"', '\\"')
    version = twempest.__version__

    with sys.stdin as f:
        formula = f.read()

    formula = formula.replace('depends_on "python3"', 'depends_on "python"')
    formula = formula.replace('desc "Shiny new formula"', f'version "{version}"\n  desc "{description}"')

    with sys.stdout as f:
        f.write(formula)
