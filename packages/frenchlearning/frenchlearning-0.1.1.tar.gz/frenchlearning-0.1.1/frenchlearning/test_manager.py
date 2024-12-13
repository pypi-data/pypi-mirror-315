#!/usr/bin/env python
# coding: utf-8

# In[5]:


import unittest
from pathlib import Path
import sys

sys.path.append(str(Path.cwd().parent))
from quiz.manager import StatusManager
from memorization.classes import WordPair, Status


class TestManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manager = StatusManager()

    @classmethod
    def tearDownClass(cls):
        cls.manager.correct_first_time.clear()
        cls.manager.failed_first_time.clear()
        del cls.manager

    def setUp(self):
        self.word_pair = WordPair("chat", "cat")

    def tearDown(self):
        self.manager.correct_first_time.clear()
        self.manager.failed_first_time.clear()
        del self.word_pair

    def test_update_status_correct(self):
        self.manager.update_status(self.word_pair, "correct")
        self.assertIn(self.word_pair, self.manager.correct_first_time)
        self.assertEqual(self.word_pair.status, Status.CORRECT_FIRST_TIME)
        self.assertNotIn(self.word_pair, self.manager.failed_first_time)

    def test_update_status_incorrect(self):
        self.manager.update_status(self.word_pair, "incorrect")
        self.assertIn(self.word_pair, self.manager.failed_first_time)
        self.assertEqual(self.word_pair.status, Status.FAILED_FIRST_TIME)
        self.assertNotIn(self.word_pair, self.manager.correct_first_time)


if __name__ == "__main__":
    unittest.main(argv=[""], verbosity=2, exit=False)


# In[ ]:
