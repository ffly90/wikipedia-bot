#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import yaml
import indexer
import searcher
import api
import frontend
from indexer import stripTag
from searcher import binaryIndexSearch

class TestUM(unittest.TestCase):
    config = {'PATH_WIKI_XML': 'testdata', 'PATH_INDEX_FILES': 'testdata/index', 'FILENAME_WIKI': 'dump.xml', 'FILENAME_INDEX': 'index.txt', 'FILENAME_SORTED_INDEX': 'sorted_index.txt', 'HOSTNAME': 'localhost', 'PORT': '5000'}
    def testIndexerMain(self):
        self.assertEqual( indexer.main(".config/config_test.yml"), None)
    def testIndexerStripTag(self):
        self.assertEqual( stripTag('{http://www.mediawiki.org/xml/export-0.10/}title'), 'title')
        self.assertEqual( stripTag('title'), 'title')
        with self.assertRaises(TypeError) and self.assertRaises(SystemExit):
            stripTag('conclusion xyz xyz')
    def testSearcherBinaryIndexSearch(self):
        self.assertEqual( binaryIndexSearch([['ab','2','3','None'],['abc','8','4','None'],['c','2','5','None'],['d','4','6','c']], 'c'), (['c','2','5','None'], False))
        self.assertEqual( binaryIndexSearch([['ab','2','3','None'],['abc','8','4','None'],['c','2','5','None'],['d','4','6','c']], 'd'), (['c','2','5','None'], False))
        self.assertEqual( binaryIndexSearch([['ab','2','3','None'],['abc','8','4','None'],['c','2','5','None'],['d','4','6','c']], 'e'), (False, False))
        self.assertEqual( binaryIndexSearch([['ab','2','3','None'],['abc','8','4','None'],['c','2','5','None'],['d','4','6','c']], 'a'), (['ab','abc'], True))
        self.assertEqual( binaryIndexSearch([], 'a'), (False, False))
        self.assertEqual( binaryIndexSearch([['ab','2','3','None'],['abc','8','4','None'],['c','2','5','None'],['d','4','6','c']], ''), (False, False))
        self.assertEqual( binaryIndexSearch([['ab','2','3','None'],['abc','8','4','None'],['c','5','None'],['d','4','6','c']], 'c'), (False, False))

if __name__ == '__main__':
    unittest.main()