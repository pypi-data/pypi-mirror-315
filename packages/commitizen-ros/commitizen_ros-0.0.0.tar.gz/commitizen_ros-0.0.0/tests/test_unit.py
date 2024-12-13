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
RAND_VERSION_COUNT = 100


@pytest.fixture
def sample_rp_tuple(request):
    uut = RosProvider(BaseConfig())
    temp_dir = mkdtemp()
    uut.filename = Path(temp_dir) / 'project.xml'
    template_fp = Path(__file__).parent / 'data' / 'project.xml'
    with open(template_fp, 'r') as src, open(uut.filename, 'w+') as dst:
        for src_line in src:
            dst_line = src_line.replace(
                '<version>-1.0.0</version>',
                f"<version>{request.param}</version>")
            dst.write(dst_line)
            print(f"Reading from {template_fp}")
            print(f"Writing to {uut.file}")
            print(f"Read {src_line} and replaced with {dst_line}")
    yield (uut, request.param)
    rmtree(path=temp_dir)


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


class TestUnit:
    """Unit test the Commitzen ROS Version Provider"""

    @pytest.mark.parametrize(
            'sample_rp_tuple',
            [get_random_version() for _ in range(RAND_VERSION_COUNT)],
            indirect=True,
            ids=[idx for idx in range(RAND_VERSION_COUNT)])
    def test_get_value(self, sample_rp_tuple) -> None:
        """Tests if provider returns version accurately"""
        uut, truth_version = sample_rp_tuple
        assert uut.get_version() == truth_version

    @pytest.mark.parametrize(
            'rand_version',
            [get_random_version() for _ in range(RAND_VERSION_COUNT)],
            ids=[idx for idx in range(RAND_VERSION_COUNT)])
    def test_set_value(self, sample_rp, rand_version) -> None:
        """Tests if provider sets version accurately"""
        sample_rp.set_version(rand_version)
        assert sample_rp.get_version() == rand_version
