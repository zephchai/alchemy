#!/usr/bin/env python

import os
import sys
import unittest
from context import Alchemist

class TestSuite(unittest.TestCase):
    def setUp(self):
        self.alchemist = Alchemist()
        module_dir = os.path.dirname(os.path.abspath(__file__))
        self.alchemist.config["alc_path"] = os.path.join(module_dir, 
                "testToolConfig")
        self.data = self.alchemist.load("basic")

    def test_readString(self):
        self.assertTrue(self.data.get("someString", ""), "Hello world")
        
    def test_readList(self):
        self.assertTrue(self.data.get("aList", ""), ["a", "b", "c"])

    def test_readDict(self):
        self.assertTrue(self.data.get("aDict", ""), {"key1": "val1", "key2": "val2"})
 
 
if __name__ == "__main__":
    unittest.main()
