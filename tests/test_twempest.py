""" Twempest render logic unit tests.
"""

# This file is part of Twempest. Copyright 2017 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import os

from click import echo
from click.testing import CliRunner
import jinja2
# noinspection PyPackageRequirements
import pytest

from twempest.twempest import cleanup_downloaded_images, download_from_url, download_images, render, TwempestError
from twempest.__main__ import CONFIG_OPTIONS
from .fixtures import MockEcho, tweets_fixture


IMAGE_TWEET_IDS = (806229878861201408, 810533832529219584, 812831603051220992, 814688934835826688)
TEST_IMAGE_URL = "http://placehold.it/10x10.jpg"
TEST_IMAGE_SIZE = 3881


def mock_download(url, file_path):
    """ Write a ~100KB file to file_path as if it were downloaded.
    """
    with open(file_path, "wb") as f:
        f.write(url.encode('utf-8'))
        f.seek(1024 * 1024)
        f.write(b'0')


@pytest.fixture
def mock_echo():
    return MockEcho()


@pytest.fixture
def tweets():
    return tweets_fixture()


# noinspection PyShadowingNames
def test_cleanup_downloaded_images(mock_echo):
    with CliRunner().isolated_filesystem():
        image_file_paths = []

        for i in range(4):
            image_file_name = "image{}.jpg".format(i)
            image_file_path = os.path.join(".", image_file_name)
            image_file_paths.append(image_file_path)
            with open(image_file_path, 'w') as f:
                f.write("foo")

        cleanup_downloaded_images(image_file_paths, echo)
        assert len(mock_echo.errs) == len(mock_echo.messages) == 0

        for path in image_file_paths:
            assert not os.path.exists(path)


# noinspection PyShadowingNames
def test_cleanup_downloaded_images_fail_cant_delete(mock_echo):
    with CliRunner().isolated_filesystem():
        image_file_path = os.path.join(".", "quux.jpg")
        cleanup_downloaded_images([image_file_path], mock_echo.echo)
        assert len(mock_echo.errs) == len(mock_echo.messages) == 1
        assert mock_echo.errs[0]
        assert mock_echo.messages[0].startswith("Warning: Unable to delete downloaded image file:")
        assert image_file_path in mock_echo.messages[0]


def test_download_from_url():
    with CliRunner().isolated_filesystem():
        path = os.path.join("download", "test.jpg")
        os.mkdir("download")
        download_from_url(TEST_IMAGE_URL, path)
        assert os.path.exists(path)
        stat_info = os.stat(path)
        assert stat_info.st_size == TEST_IMAGE_SIZE


def test_download_from_url_fail_url():
    with CliRunner().isolated_filesystem():
        path = os.path.join("download", "test.jpg")
        os.mkdir("download")

        with pytest.raises(TwempestError) as excinfo:
            download_from_url("http://test.com/doesntexist", path)

        assert "Unable to download image file:" in str(excinfo.value)
        assert not os.path.exists(path)


def test_download_from_url_fail_save():
    with CliRunner().isolated_filesystem():
        path = os.path.join("download", "test.jpg")
        os.mkdir("download", 0o111)

        with pytest.raises(TwempestError) as excinfo:
            download_from_url(TEST_IMAGE_URL, path)

        assert "Unable to write downloaded image file:" in str(excinfo.value)
        assert not os.path.exists(path)


# noinspection PyShadowingNames
def test_download_images(mock_echo, tweets):
    env = jinja2.Environment()
    image_dir_path_template = env.from_string("images")
    image_url_path_template = env.from_string("/images/")
    image_paths = []

    with CliRunner().isolated_filesystem():
        for tweet in tweets:
            render_file_name = "tweet_{}_file.md".format(tweet.id)
            paths = download_images(tweet, image_dir_path_template, image_url_path_template, render_file_name, mock_download,
                                    mock_echo.echo)

            if paths:
                image_paths.append(paths[0])

        assert len(image_paths) == len(IMAGE_TWEET_IDS)

        for tweet_id in IMAGE_TWEET_IDS:
            path = os.path.join("images", "tweet_{}_file-0.jpg".format(tweet_id))
            assert os.path.exists(path)
            stat_info = os.stat(path)
            assert stat_info.st_size > 1024 * 1024
            assert len([1 for p in image_paths if p.endswith(path)]) == 1, "path '{}' not found in image_paths list.".format(path)


# noinspection PyShadowingNames
def test_download_images_some_exist(mock_echo, tweets):
    env = jinja2.Environment()
    image_dir_path_template = env.from_string("images")
    image_url_path_template = env.from_string("/images/")
    image_paths = []

    with CliRunner().isolated_filesystem():
        for tweet in tweets:
            render_file_name = "tweet_{}_file.md".format(tweet.id)

            if tweet.id == IMAGE_TWEET_IDS[-1]:
                with open(os.path.join("images", "tweet_{}_file-0.jpg".format(tweet.id)), "wb") as f:
                    f.seek(1024 * 1024)
                    f.write(b'0')

            paths = download_images(tweet, image_dir_path_template, image_url_path_template, render_file_name, mock_download,
                                    mock_echo.echo)

            if paths:
                image_paths.append(paths[0])

            if tweet.id == IMAGE_TWEET_IDS[-1]:
                assert len(mock_echo.messages) == 1
                assert "Warning: Skipping existing image file" in mock_echo.messages[0]
                assert str(tweet.id) in mock_echo.messages[0]

        assert len(image_paths) == len(IMAGE_TWEET_IDS) - 1


# noinspection PyShadowingNames
def test_download_images_media_update(mock_echo, tweets):
    env = jinja2.Environment()
    image_dir_path_template = env.from_string("images")
    image_url_path_template = env.from_string("/images/")
    media_before = {}
    media_after = {}

    with CliRunner().isolated_filesystem():
        for tweet in tweets:
            render_file_name = "tweet_{}_file.md".format(tweet.id)
            media_before[tweet.id] = [{'media_url': m['media_url'],
                                       'media_url_https': m['media_url_https']}
                                      for m in tweet.entities.get('media', []) if m['type'] == 'photo']

            download_images(tweet, image_dir_path_template, image_url_path_template, render_file_name, mock_download, mock_echo.echo)

            media_after[tweet.id] = [{'media_url': m['media_url'],
                                      'media_url_https': m['media_url_https'],
                                      'original_media_url': m['original_media_url'],
                                      'original_media_url_https': m['original_media_url_https']}
                                     for m in tweet.entities.get('media', []) if m['type'] == 'photo']

        for tweet_id in IMAGE_TWEET_IDS:
            before = media_before[tweet_id]
            after = media_after[tweet_id]

            for i, b in enumerate(before):
                a = after[i]
                assert b['media_url'] == a['original_media_url']
                assert b['media_url'] != a['media_url']
                assert b['media_url_https'] == a['original_media_url_https']
                assert b['media_url_https'] != a['media_url_https']


# noinspection PyShadowingNames
def test_render(mock_echo, tweets):
    with CliRunner().isolated_filesystem():
        template_text = "{{ tweet.id }}"
        options = {k: v.default for k, v in CONFIG_OPTIONS.items()}
        last_id = render(tweets, options, template_text, mock_download, mock_echo.echo)
        rendered_ids = [i for i in mock_echo.messages if i]
        assert len(rendered_ids) == len(tweets)
        assert str(last_id) == rendered_ids[-1]

        for tweet in tweets:
            assert str(tweet.id) in rendered_ids
