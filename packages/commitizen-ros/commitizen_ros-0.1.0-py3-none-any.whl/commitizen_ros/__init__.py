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


import logging
from pathlib import Path
from xml.etree import ElementTree

from commitizen.providers.base_provider import FileProvider


logger = logging.getLogger(__file__)


class RosProvider(FileProvider):
    """Implements a Commitizen Version Provider for REP140 compliant Package
    Manifests.
    """

    def get_etree(self) -> ElementTree:
        """Parses package manifest XML"""
        try:
            etree = ElementTree.parse(self.file)
        except ElementTree.ParseError as e:
            logger.error(
                'Unable to parse ROS package manifest %s; '
                 + 'Please confirm compliance with REP140.', self.file)
            raise
        return etree

    def get_version(self) -> str:
        etree = self.get_etree()
        version_str = etree.find('version').text
        return version_str
    
    def set_version(self, version: str) -> str:
        etree = self.get_etree()
        version_tag = etree.find('version')
        version_tag.text = version
        etree.write(str(self.file))
