#!/usr/bin/env python
# coding: utf-8

# In[2]:


import unittest
from memorization.classes import WordPair, EasyWordPair


class TestClasses(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.easy_pair = EasyWordPair("chat", "cat")

    @classmethod
    def tearDownClass(cls):
        del cls.easy_pair

    def setUp(self):
        self.word_pair = WordPair("chien", "dog")

    def tearDown(self):
        del self.word_pair

    def test_wordpair_equality(self):
        another_pair = WordPair("chien", "dog")
        self.assertEqual(self.word_pair, another_pair)
        self.assertEqual(hash(self.word_pair), hash(another_pair))
        self.assertIsInstance(self.word_pair, WordPair)
        self.assertNotEqual(self.word_pair, WordPair("chat", "cat"))

    def test_easywordpair_difficulty(self):
        self.assertEqual(self.easy_pair.difficulty, "Easy")
        self.assertEqual(self.easy_pair.french, "chat")
        self.assertEqual(self.easy_pair.english, "cat")
        self.assertIsInstance(self.easy_pair, EasyWordPair)


if __name__ == "__main__":
    unittest.main(argv=[""], verbosity=2, exit=False)


# In[ ]:
