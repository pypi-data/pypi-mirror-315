#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Description: This UT will check all core scripts to validate that common functions is loaded
#
# Copyright (C) 2017-2021, 2023, 2024 Pablo Iranzo Gómez <Pablo.Iranzo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os
import re
import sys
from unittest import TestCase

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/" + "../" + "../"))

try:
    import risuclient.shell as risu
except:
    import shell as risu

testplugins = os.path.join(risu.risudir, "plugins", "test")
pluginsdir = os.path.join(risu.risudir, "plugins", "core")
plugins = risu.findplugins(folders=[pluginsdir])


class RisuTest(TestCase):
    def test_ut_sourced_if_used(self):
        # Check list of plugins for regexp sourcing common functions and skip them
        nonsourcing = []
        for plugin in plugins:
            if not risu.regexpfile(
                filename=plugin["plugin"], regexp=".*common-functions"
            ):
                nonsourcing.append(plugin["plugin"])

        commonfunctions = []

        for script in risu.findplugins(
            folders=[os.path.join(risu.risudir, "common.d")],
            fileextension=".sh",
        ):
            filename = script["plugin"]
            with open(filename, "r") as f:
                for line in f:
                    find = re.match("^(([a-z]+_+)+[a-z]*)", line)
                    if find and find.groups()[0] != "":
                        commonfunctions.append(find.groups()[0])

        usingcf = []
        for plugin in nonsourcing:
            for func in commonfunctions:
                if risu.regexpfile(filename=plugin, regexp=".*%s" % func):
                    usingcf.append(plugin)

        assert sorted(set(usingcf)) == []
