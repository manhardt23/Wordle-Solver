import unittest
from wordle import bot

class TestRemoveWords(unittest.TestCase):

    def test_all_correct(self):
        word_list_recycle = ['apple', 'grape', 'lemon']
        guess_list = 'apple'
        current_values = '22222'
        secret_word = 'apple'
        result = bot.remove_words(word_list_recycle, guess_list, current_values, secret_word)
        self.assertEqual(result, ['apple'])

    def test_all_incorrect(self):
        word_list_recycle = ['apple', 'grape', 'lemon']
        guess_list = 'apple'
        current_values = '00000'
        secret_word = 'grape'
        result = bot.remove_words(word_list_recycle, guess_list, current_values, secret_word)
        self.assertEqual(result, ['grape', 'lemon'])

    def test_some_correct_some_wrong_position(self):
        word_list_recycle = ['apple', 'grape', 'lemon']
        guess_list = 'apple'
        current_values = '20100'
        secret_word = 'grape'
        result = bot.remove_words(word_list_recycle, guess_list, current_values, secret_word)
        self.assertEqual(result, ['grape'])

    def test_some_wrong(self):
        word_list_recycle = ['apple', 'grape', 'lemon']
        guess_list = 'apple'
        current_values = '20000'
        secret_word = 'apple'
        result = bot.remove_words(word_list_recycle, guess_list, current_values, secret_word)
        self.assertEqual(result, ['apple'])

    def test_empty_list(self):
        word_list_recycle = ['apple', 'grape', 'lemon']
        guess_list = 'apple'
        current_values = '21100'
        secret_word = 'lemon'
        result = bot.remove_words(word_list_recycle, guess_list, current_values, secret_word)
        self.assertEqual(result, [])

    def test_no_matches(self):
        word_list_recycle = ['apple', 'grape', 'lemon']
        guess_list = 'apple'
        current_values = '10000'
        secret_word = 'lemon'
        result = bot.remove_words(word_list_recycle, guess_list, current_values, secret_word)
        self.assertEqual(result, ['grape', 'lemon'])

if __name__ == '__main__':
    unittest.main()
