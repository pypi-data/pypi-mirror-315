#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2021, 2023 Pablo Iranzo Gómez <Pablo.Iranzo@gmail.com>
import os
import sys
from unittest import TestCase

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/" + "../"))

from risuclient.tools.dmidecode import (
    parse_dmi,
)


class CitellusTest(TestCase):
    def test_dmidecode(self):
        with open("tests/other/dmidecode", "r") as f:
            content = f.read()
            output = parse_dmi(content)
            assert output != "1"
