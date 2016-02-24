#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import tempfile
import unittest

from sjkscan.utils import files, move


class TestFiles(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_files = ['test1.pnm', 'test2.pnm', 'test3.jpg']
        for f in self.test_files:
            open(os.path.join(self.temp_dir, f), 'a').close()

    def test_listing_all_pnm_files_in_directory(self):
        pnms = []
        expected = ['test1.pnm', 'test2.pnm']
        for f in files(self.temp_dir, 'pnm'):
            pnms.append(f)
        self.assertEqual(pnms, expected)

    def test_listing_all_pnms_doesnt_list_jpg(self):
        pnms = []
        for f in files(self.temp_dir, 'pnm'):
            pnms.append(f)
        self.assertNotIn('test3.jpg', pnms)

    def test_listing_all_dot_pnms(self):
        pnms = []
        expected = ['test1.pnm', 'test2.pnm']
        for f in files(self.temp_dir, '.pnm'):
            pnms.append(f)
        self.assertEqual(pnms, expected)

    def test_listing_all_files(self):
        all = []
        for f in files(self.temp_dir):
            all.append(f)
        self.assertEqual(self.test_files, all)

    def test_listing_files_doesnt_include_directories(self):
        dir = os.path.join(self.temp_dir, 'test')
        os.mkdir(dir)

        all = []
        for f in files(self.temp_dir):
            all.append(f)
        self.assertEqual(self.test_files, all)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)


class TestMove(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, 'test.txt')
        open(self.test_file, 'a').close()

    def test_if_file_can_be_moved(self):
        new_test_file = os.path.join(self.temp_dir, 'test2.txt')
        move(self.test_file, new_test_file)
        self.assertTrue(os.path.exists(new_test_file))

    def tearDown(self):
        shutil.rmtree(self.temp_dir)


if __name__ == "__main__":
    unittest.main()
