#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
import unittest


class TestBinariesInPath(unittest.TestCase):

    """
    TODO: Docstring

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_identify_binary_in_path(self):
        self.assertIsNotNone(shutil.which('identify'))

if __name__ == "__main__":
    unittest.main()
