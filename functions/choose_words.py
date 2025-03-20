import random
import string

def generate_random_string(L):
    """Generate a random English string of length L."""
    return ''.join(random.choices(string.ascii_letters, k=L))

def choose_words(search_words):
    if search_words == '':
        return generate_random_string(2)
    else:
        words = search_words.split(',')
        return words[random.randint(0, len(words)-1)]