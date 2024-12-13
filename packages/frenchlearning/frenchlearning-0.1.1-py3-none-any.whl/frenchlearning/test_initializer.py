#!/usr/bin/env python
# coding: utf-8

# In[5]:


import unittest
from pathlib import Path
import sys

sys.path.append(str(Path.cwd().parent))
from memorization.classes import EasyWordPair, MediumWordPair, HardWordPair
from memorization.initializer import initialize_word_pairs


class TestInitializer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.word_pairs = initialize_word_pairs()

    @classmethod
    def tearDownClass(cls):
        del cls.word_pairs

    def setUp(self):
        self.easy_pair = self.word_pairs[0]

    def tearDown(self):
        del self.easy_pair

    def test_initialize_word_pairs_length(self):
        self.assertEqual(len(self.word_pairs), 30)
        self.assertIsInstance(self.word_pairs[0], EasyWordPair)
        self.assertIsInstance(self.word_pairs[10], MediumWordPair)
        self.assertIsInstance(self.word_pairs[20], HardWordPair)

    def test_initialize_word_pairs_content(self):
        self.assertEqual(self.easy_pair.french, "bonjour")
        self.assertEqual(self.easy_pair.english, "hello")
        self.assertEqual(self.easy_pair.difficulty, "Easy")
        self.assertNotEqual(self.easy_pair.difficulty, "Medium")


if __name__ == "__main__":
    unittest.main(argv=[""], verbosity=2, exit=False)


# In[ ]:
