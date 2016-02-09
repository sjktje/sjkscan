#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
import unittest


class TestScanimage(unittest.TestCase):

    """
    TODO: Docstring

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_tesseract_binary_in_path(self):
        self.assertIsNotNone(shutil.which('tesseract'))

if __name__ == "__main__":
    unittest.main()
