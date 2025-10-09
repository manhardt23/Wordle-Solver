import unittest as ut
from wordle import bot
from wordle import game


class TestLetterColoring(ut.TestCase):
    """Test the letter_coloring function with various scenarios"""
    
    def test_all_gray(self):
        """All letters incorrect"""
        guess = 'chins'
        secret_word = 'grape'
        result = game.letter_coloring(guess, secret_word)
        self.assertEqual(result, '00000')
    
    def test_all_green(self):
        """All letters correct and in correct position"""
        guess = 'grape'
        secret_word = 'grape'
        result = game.letter_coloring(guess, secret_word)
        self.assertEqual(result, '22222')
    
    def test_all_yellow(self):
        """All letters correct but in wrong positions"""
        guess = 'eadcb'
        secret_word = 'abcde'
        result = game.letter_coloring(guess, secret_word)
        self.assertEqual(result, '11111')
    
    def test_repeated_letters_both_correct(self):
        """Repeated letter in guess, both in secret word"""
        guess = 'allay'
        secret_word = 'chill'
        result = game.letter_coloring(guess, secret_word)
        self.assertEqual(result, '01100')

    
    def test_triple_letters_in_guess(self):
        """Three same letters in guess, only one in secret"""
        guess = 'eerie'
        secret_word = 'raise'
        result = game.letter_coloring(guess, secret_word)
        self.assertEqual(result, '00112')
    
    def test_triple_letters_mixed_results(self):
        """Three same letters: one green, one yellow, one gray"""
        guess = 'lolly'
        secret_word = 'loyal'
        result = game.letter_coloring(guess, secret_word)
        self.assertEqual(result, '22101')
    
    def test_mixed_feedback(self):
        """Mix of green, yellow, and gray"""
        guess = 'slate'
        secret_word = 'paste'
        result = game.letter_coloring(guess, secret_word)
        self.assertEqual(result, '10122')
    
    def test_no_vowels_match(self):
        """Word with vowels vs word without matching vowels"""
        guess = 'audio'
        secret_word = 'tryst'
        result = game.letter_coloring(guess, secret_word)
        self.assertEqual(result, '00000')


class TestRemoveWords(ut.TestCase):
    """Test the remove_words function with various scenarios"""

    def test_all_correct(self):
        """All green - should only keep exact match"""
        word_list = ['apple', 'grape', 'lemon']
        guess = 'apple'
        current_values = '22222'
        result = bot.remove_words(word_list, guess, current_values)
        self.assertEqual(result, ['apple'])

    def test_all_incorrect(self):
        """All gray - remove words with any of those letters"""
        word_list = ['apple', 'grape', 'lemon', 'drunk']
        guess = 'apple'
        current_values = '00000'
        result = bot.remove_words(word_list, guess, current_values)
        self.assertEqual(result, ['drunk'])

    def test_empty_result(self):
        """No words match the criteria"""
        word_list = ['apple', 'grape', 'lemon']
        guess = 'apple'
        current_values = '00000'
        result = bot.remove_words(word_list, guess, current_values)
        self.assertEqual(result, [])
        
    
    def test_preserve_word_order(self):
        """Verify that word order is preserved"""
        word_list = ['zebra', 'apple', 'delta', 'alpha', 'omega']
        guess = 'zzzzz'
        current_values = '00000'
        result = bot.remove_words(word_list, guess, current_values)
        # All words should remain except zebra (has 'z')
        self.assertEqual(result, ['apple', 'delta', 'alpha', 'omega'])
    
    
    def test_empty_word_list(self):
        """Test with empty word list"""
        word_list = []
        guess = 'apple'
        current_values = '22222'
        result = bot.remove_words(word_list, guess, current_values)
        self.assertEqual(result, [])
    
    def test_multiple_yellows_same_letter(self):
        """Multiple occurrences of same letter, both yellow"""
        word_list = ['llama', 'allay', 'legal', 'label', 'local']
        guess = 'alloy'
        current_values = '11100'  # Both l's yellow, rest gray
        result = bot.remove_words(word_list, guess, current_values)
        # Must have two l's but not at positions 1 and 2
        self.assertEqual(result, ['legal', 'label'])


class TestPositionFrequencies(ut.TestCase):
    """Test the calculate_position_frequencies function"""
    
    def test_basic_frequency_calculation(self):
        """Test basic frequency counting"""
        bot.word_list_recycle = ['apple', 'apply', 'ample']
        result = bot.calculate_position_frequencies()
        
        # Position 0: all have 'a'
        self.assertEqual(result[0]['a'], 3)
        
        # Position 1: two 'p', one 'm'
        self.assertEqual(result[1]['p'], 2)
        self.assertEqual(result[1]['m'], 1)
    
    def test_empty_word_list(self):
        """Test with empty word list"""
        bot.word_list_recycle = []
        result = bot.calculate_position_frequencies()
        
        # Should return 5 empty dictionaries
        self.assertEqual(len(result), 5)
        for pos_dict in result:
            self.assertEqual(len(pos_dict), 0)
    
    def test_single_word(self):
        """Test with single word"""
        bot.word_list_recycle = ['crane']
        result = bot.calculate_position_frequencies()
        
        # Each position should have frequency of 1
        self.assertEqual(result[0]['c'], 1)
        self.assertEqual(result[1]['r'], 1)
        self.assertEqual(result[2]['a'], 1)
        self.assertEqual(result[3]['n'], 1)
        self.assertEqual(result[4]['e'], 1)


class TestScoreWord(ut.TestCase):
    """Test the score_word function"""
    
    def test_unique_letters_bonus(self):
        """Words with unique letters should score higher"""
        position_freq = [{'a': 5}, {'b': 5}, {'c': 5}, {'d': 5}, {'e': 5}]
        
        score1 = bot.score_word('abcde', position_freq)
        score2 = bot.score_word('aabbc', position_freq)
        
        # abcde has 5 unique letters, aabbc has 3
        # So abcde should score higher
        self.assertGreater(score1, score2)
    
    def test_frequency_contribution(self):
        """Higher frequency letters should increase score"""
        position_freq = [
            {'a': 10, 'z': 1},
            {'b': 10, 'y': 1},
            {'c': 10, 'x': 1},
            {'d': 10, 'w': 1},
            {'e': 10, 'v': 1}
        ]
        
        score_common = bot.score_word('abcde', position_freq)
        score_rare = bot.score_word('zyxwv', position_freq)
        
        self.assertGreater(score_common, score_rare)


class TestWordList(ut.TestCase):
    """Test word list loading"""
    
    def test_word_list_not_empty(self):
        """Verify word list loads successfully"""
        words = game.word_list()
        self.assertGreater(len(words), 0)
    
    def test_all_words_five_letters(self):
        """Verify all words are 5 letters"""
        words = game.word_list()
        for word in words[:100]:  # Test first 100 words
            self.assertEqual(len(word), 5)
    
    def test_no_empty_strings(self):
        """Verify no empty strings in word list"""
        words = game.word_list()
        for word in words:
            self.assertNotEqual(word, '')


if __name__ == '__main__':
    num, errs, fails = 0, 0, 0
    test_cases = [
        TestLetterColoring,
        TestRemoveWords,
        TestPositionFrequencies,
        TestScoreWord,
        TestWordList
    ]
    
    for test_case in test_cases:
        test_suite = ut.TestLoader().loadTestsFromTestCase(test_case)
        res = ut.TextTestRunner(verbosity=2).run(test_suite)
        num += res.testsRun
        errs += len(res.errors)
        fails += len(res.failures)

    print("\n" + "="*50)
    print("score: %d of %d (%d errors, %d failures)" % (num - (errs+fails), num, errs, fails))