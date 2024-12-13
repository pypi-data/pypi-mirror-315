#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import random
from difflib import SequenceMatcher
from memorization.classes import NearlyCorrectError


def display_word_pairs(word_pairs, test_mode=False):
    if test_mode:
        return True
    print("\nPlease memorize the following French-English word pairs:\n")
    for pair in word_pairs:
        print(pair.french + " - " + pair.english)
    print(
        "\nWhen you are done memorizing, type 'start' to begin the quiz, or 'exit' to finish and see your results.\n"
    )
    while True:
        try:
            user_input = input("Type 'start' to begin the quiz: ").strip().lower()
            if user_input == "start":
                return True
            elif user_input == "exit":
                return False
            else:
                raise ValueError(
                    "Invalid input. Please type 'start' to begin or 'exit' to finish."
                )
        except ValueError as ve:
            print("Error")


def clear_screen():
    print("\n" * 50)


def is_nearly_correct(answer, correct_answer):
    return SequenceMatcher(None, answer, correct_answer).ratio() >= 0.9


def quiz_user(word_pairs, status_manager):
    clear_screen()
    print(
        "Quiz Time! Please provide the English meaning for the following French words:"
    )
    print("Type 'exit' to finish and see your results, or 'hint' for a hint.\n")
    wrong_pairs = []
    for pair in word_pairs:
        while True:
            try:
                answer = input(pair.french + ": ").strip().lower()
                if answer == "exit":
                    print("Exiting the quiz...\n")
                    return None
                elif answer == "hint":
                    print("Hint: The word starts with" + pair.english[0])
                    continue
                if not answer.isalpha():
                    raise ValueError(
                        "Your input must only contain alphabetic characters. Try again."
                    )
                if not answer:
                    raise ValueError("Input cannot be empty. Please try again.")
                if answer == pair.english.lower():
                    print("Correct!\n")
                    status_manager.update_status(pair, "correct")
                    break
                elif is_nearly_correct(answer, pair.english.lower()):
                    raise NearlyCorrectError(
                        "Nearly correct! The abusolute correct answer is "
                        + pair.english
                        + ", but we'll count it as correct for now."
                    )
                else:
                    print("Incorrect. The correct answer is\n")
                    print(pair.english)
                    status_manager.update_status(pair, "incorrect")
                    wrong_pairs.append(pair)
                    break
            except ValueError as ve:
                print(ve)
            except NearlyCorrectError as ne:
                print(ne)
                status_manager.update_status(pair, "correct")
                break
    return wrong_pairs
