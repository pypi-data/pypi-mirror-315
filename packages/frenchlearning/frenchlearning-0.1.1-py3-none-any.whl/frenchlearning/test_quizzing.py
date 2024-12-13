#!/usr/bin/env python
# coding: utf-8

# In[1]:


import unittest
from pathlib import Path
import sys

sys.path.append(str(Path.cwd().parent))
from quiz.quizzing import display_word_pairs
from memorization.classes import WordPair
from unittest.mock import patch


class TestQuizzing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.word_pairs = [WordPair("chat", "cat"), WordPair("chien", "dog")]

    @classmethod
    def tearDownClass(cls):
        del cls.word_pairs

    def test_display_word_pairs(self):
        self.assertTrue(display_word_pairs(self.word_pairs, True))
        self.assertEqual(len(self.word_pairs), 2)
        self.assertIsInstance(self.word_pairs[0], WordPair)


if __name__ == "__main__":
    unittest.main(argv=[""], verbosity=2, exit=False)

# In[ ]:
