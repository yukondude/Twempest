#!/usr/bin/env python
""" Twempest setuptools configuration.
"""

# This file is part of Twempest. Copyright 2018 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public
# License, version 3. Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

import os

# noinspection PyPackageRequirements
from pipenv.project import Project
# noinspection PyPackageRequirements
from pipenv.utils import convert_deps_to_pip
from setuptools import setup, find_packages
# noinspection PyPep8Naming
from setuptools.command.test import test as TestCommand
import sys

import twempest


if sys.version_info < (3, 6):
    sys.stderr.write("Twempest requires Python 3.6 or higher.\n")
    sys.exit(1)


HERE = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(HERE, "README.rst"), encoding='utf-8') as f:
    long_description = f.read().strip()


def gather_requirements(requirements_file_name):
    """ Return the list of required packages and versions from requirements.txt.
    """
    return [pkg.strip() for pkg in open(os.path.join(HERE, requirements_file_name), "r").readlines()]


PYTEST_ARGS = ["--cov=twempest", "--cov=tests", "--cov-report=term-missing", "--cov-fail-under=80", "--flake8",
               "-W ignore::DeprecationWarning"]


# noinspection PyAttributeOutsideInit
class PyTest(TestCommand):
    test_args = PYTEST_ARGS
    test_suite = True

    def finalize_options(self):
        TestCommand.finalize_options(self)

    def run_tests(self):
        # noinspection PyPackageRequirements
        import pytest
        sys.exit(pytest.main(self.test_args))


# noinspection PyAttributeOutsideInit
class PyCleanTest(PyTest):
    """ Same as PyTest, but clear the cache first.
    """
    test_args = ["--verbose", "--cache-clear"] + PYTEST_ARGS


setup(
    author="Dave Rogers",
    author_email="thedude@yukondude.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    cmdclass={
        'test': PyTest,
        'cleantest': PyCleanTest,
    },
    description=twempest.__doc__.strip(),
    entry_points={
        'console_scripts': [
            "twempest=twempest.__main__:twempest",
        ]
    },
    include_package_data=True,
    install_requires=convert_deps_to_pip(Project(chdir=False).parsed_pipfile['packages'], r=False),
    license="GPLv3",
    long_description=long_description,
    name="twempest",
    packages=find_packages(),
    platforms=["MacOS", "Linux"],
    tests_require=convert_deps_to_pip(Project(chdir=False).parsed_pipfile['dev-packages'], r=False),
    url="https://github.com/yukondude/Twempest",
    version=twempest.__version__,
    zip_safe=False,
)
