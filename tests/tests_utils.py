#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import tempfile
import unittest

from sjkscan.utils import files, move, remove, is_scan_name, version
from sjkscan.config import load_config
from sjkscan import __version__


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


class TestRemove(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, 'test.txt')
        open(self.test_file, 'a').close()

    def test_if_file_can_be_removed(self):
        remove(self.test_file)
        self.assertFalse(os.path.exists(self.test_file))

    def tearDown(self):
        shutil.rmtree(self.temp_dir)


class TestIsScanName(unittest.TestCase):
    def setUp(self):
        load_config()

    def test_correct_scan_name_should_be_true(self):
        self.assertTrue(is_scan_name('2015-02-23_14-13-12'))

    def test_incorrect_scan_name_should_be_false(self):
        self.assertFalse(is_scan_name('blah'))


class TestVersion(unittest.TestCase):
    def test_version_returns_correct_version(self):
        self.assertEqual(version(), __version__)


if __name__ == "__main__":
    unittest.main()
