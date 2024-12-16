import unittest
from reverse_words_package.reverse_words.reverse import reverse_words

class TestReverseWords(unittest.TestCase):

    def test_simple_cases(self):
        self.assertEqual(reverse_words("abcd efgh"), "dcba hgfe")
        self.assertEqual(reverse_words("a1bcd efg!h"), "d1cba hgf!e")

    def test_empty_string(self):
        self.assertEqual(reverse_words(""), "")

    def test_only_non_alpha(self):
        self.assertEqual(reverse_words("1234 5678"), "1234 5678")

    def test_single_word(self):
        self.assertEqual(reverse_words("hello"), "olleh")

    def test_spaces_and_punctuation(self):
        self.assertEqual(reverse_words("hello, world!"), "olleh, dlrow!")

if __name__ == '__main__':
    unittest.main()
