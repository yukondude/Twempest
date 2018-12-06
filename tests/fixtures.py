""" Twempest unit test fixtures.
"""

# This file is part of Twempest. Copyright 2018 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public
# License, version 3. Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import os
import pickle


def tweets_fixture():
    """ Just a whole mess--well, eighteen--of pickled sample tweets from late 2016 to test with.
    """
    pickle_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "twempest.p")
    return pickle.load(open(pickle_path, "rb"))
