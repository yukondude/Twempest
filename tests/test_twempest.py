""" Twempest render logic unit tests.
"""

# This file is part of Twempest. Copyright 2017 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import os

# noinspection PyPackageRequirements
import pytest
from click import echo
from click.testing import CliRunner

from twempest.twempest import cleanup_downloaded_images
from .fixtures import tweets_fixture


@pytest.fixture
def tweets():
    return tweets_fixture()


def test_cleanup_downloaded_images():
    with CliRunner().isolated_filesystem():
        image_file_paths = []

        for i in range(4):
            image_file_name = "image{}.jpg".format(i)
            image_file_path = os.path.join(".", image_file_name)
            image_file_paths.append(image_file_path)
            with open(image_file_path, 'w') as f:
                f.write("foo")

        cleanup_downloaded_images(image_file_paths, echo)

        for path in image_file_paths:
            assert not os.path.exists(path)


def test_cleanup_downloaded_images_fail_cant_delete():
    mock_message = []
    mock_err = []

    def mock_echo(message=None, err=False):
        mock_message.append(message)
        mock_err.append(err)

    with CliRunner().isolated_filesystem():
        image_file_path = os.path.join(".", "quux.jpg")
        cleanup_downloaded_images([image_file_path], mock_echo)

        assert len(mock_err) == len(mock_message) == 1
        assert mock_err[0]
        assert mock_message[0].startswith("Warning: Unable to delete downloaded image file:")
        assert image_file_path in mock_message[0]
