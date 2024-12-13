# MIT License
# 
# Copyright (c) 2024 Michael Stinger
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from pathlib import Path
import pytest
from random import randint
from shutil import (copyfile,
                    rmtree)
from tempfile import mkdtemp

from commitizen.config.base_config import BaseConfig
from commitizen_ros import RosProvider


MIN_RAND_VERSION = 0
MAX_RAND_VERSION = 99
RAND_VERSION_COUNT = 20


@pytest.fixture
def sample_rp():
    uut = RosProvider(BaseConfig())
    temp_dir = mkdtemp()
    uut.filename = Path(temp_dir) / 'project.xml'
    copyfile(src=Path(__file__).parent / 'data' / 'project.xml',
             dst=uut.filename)
    yield uut
    rmtree(path=temp_dir)


def get_random_version():
    return "{0}.{1}.{2}".format(
        randint(MIN_RAND_VERSION, MAX_RAND_VERSION),
        randint(MIN_RAND_VERSION, MAX_RAND_VERSION),
        randint(MIN_RAND_VERSION, MAX_RAND_VERSION))


class TestSmoke:
    """Smoke test the Commitzen ROS Version Provider"""

    def test_smoke(self, sample_rp) -> None:
        """Tests if provider runs without error"""
        sample_rp.get_version()
        sample_rp.set_version('0.0.0')

    @pytest.mark.parametrize(
            'rand_version',
            [get_random_version() for _ in range(RAND_VERSION_COUNT)],
            ids=[idx for idx in range(RAND_VERSION_COUNT)])
    def test_smoke_set(self, sample_rp, rand_version) -> None:
        """Tests if provider runs with various version arguments"""
        sample_rp.set_version(rand_version)
