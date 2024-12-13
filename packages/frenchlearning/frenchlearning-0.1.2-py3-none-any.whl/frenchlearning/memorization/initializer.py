#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pathlib import Path
import sys
sys.path.append(str(Path.cwd().parent))
from memorization.classes import EasyWordPair, MediumWordPair, HardWordPair

def initialize_word_pairs():
    word_pairs = []

    easy_words = [
        ('bonjour', 'hello'), ('chat', 'cat'), ('chien', 'dog'),
        ('merci', 'thanks'), ('pomme', 'apple'), ('fromage', 'cheese'),
        ('pain', 'bread'), ('eau', 'water'), ('lait', 'milk'), ('salut', 'hi'),
    ]

    medium_words = [
        ('maison', 'house'), ('voiture', 'car'), ('livre', 'book'),
        ('école', 'school'), ('arbre', 'tree'), ('chaise', 'chair'),
        ('table', 'table'), ('fenêtre', 'window'), ('porte', 'door'), ('jardin', 'garden'),
    ]

    hard_words = [
        ('ordinateur', 'computer'), ('hippopotame', 'hippopotamus'),
        ('développement', 'development'), ('bibliothèque', 'library'),
        ('psychologie', 'psychology'), ('pharmacie', 'pharmacy'),
        ('aéroport', 'airport'), ('ascenseur', 'elevator'),
        ('cimetière', 'cemetery'), ('immeuble', 'building'),
    ]

    for french, english in easy_words:
        word_pairs.append(EasyWordPair(french, english))

    for french, english in medium_words:
        word_pairs.append(MediumWordPair(french, english))

    for french, english in hard_words:
        word_pairs.append(HardWordPair(french, english))

    return word_pairs


# In[ ]:




