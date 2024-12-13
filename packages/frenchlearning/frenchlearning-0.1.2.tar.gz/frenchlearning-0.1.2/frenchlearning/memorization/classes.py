#!/usr/bin/env python
# coding: utf-8

# In[2]:


class WordPair:
    def __init__(self, french, english):
        self.french = french
        self.english = english
        self.status = None  # Correct or failed on first attempt

    def __hash__(self):
        return hash((self.french, self.english))

    def __eq__(self, other):
        return (self.french, self.english) == (other.french, other.english)


class EasyWordPair(WordPair):
    def __init__(self, french, english):
        super().__init__(french, english)
        self.difficulty = 'Easy'


class MediumWordPair(WordPair):
    def __init__(self, french, english):
        super().__init__(french, english)
        self.difficulty = 'Medium'


class HardWordPair(WordPair):
    def __init__(self, french, english):
        super().__init__(french, english)
        self.difficulty = 'Hard'


class Status:
    CORRECT_FIRST_TIME = 'correct_first_time'
    FAILED_FIRST_TIME = 'failed_first_time'


class NearlyCorrectError(Exception):
    def __init__(self, message="Your answer is nearly correct!"):
        self.message = message
        super().__init__(self.message)

# In[ ]:




