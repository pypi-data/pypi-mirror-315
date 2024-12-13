#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import unittest
from test_manager import TestManager
from test_quizzing import TestQuizzing
from test_classes import TestClasses
from test_initializer import TestInitializer


def my_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestClasses))
    suite.addTest(unittest.makeSuite(TestInitializer))
    return suite


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestManager))
    suite.addTest(unittest.makeSuite(TestQuizzing))
    return suite


if __name__ == "__main__":
    unittest.main(argv=[""], verbosity=2, exit=False)


# In[ ]:
