import re

def reverse_words(text):
    """
    Розвертає всі слова в рядку, залишаючи небуквенні символи на місці.
    
    :param text: рядок, що містить слова для розвертання
    :return: рядок з розвернутими словами
    
    >>> reverse_words("abcd efgh")
    'dcba hgfe'
    >>> reverse_words("a1bcd efg!h")
    'dcb1a hgf!e'
    >>> reverse_words("")
    ''
    >>> reverse_words("abc! def? ghi.")
    'cba! fed? ihg.'
    >>> reverse_words("1234")
    '1234'
    """
    
    if not isinstance(text, str):
        raise ValueError("Input must be a string")
    
    def reverse_word(word):
        # Розвертаємо лише букви в слові, зберігаючи місця небуквенних символів
        letters = [char for char in word if char.isalpha()]
        reversed_word = list(word)
        for i, char in enumerate(word):
            if char.isalpha():
                reversed_word[i] = letters.pop()
        return ''.join(reversed_word)
    
    # Розбиваємо текст на частини з урахуванням пробілів
    words = re.split(r'(\s+)', text)
    # Обробляємо кожне слово
    reversed_text = ''.join(reverse_word(word) if word.strip() else word for word in words)
    return reversed_text

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    
    while True:
        # Запит на введення тексту
        user_input = input("Введіть текст (або 'exit' для виходу): ")
        if user_input.lower() == 'exit':
            print("Вихід з програми.")
            break
        print(reverse_words(user_input))
