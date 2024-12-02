import numpy as np
import string
from collections import Counter

def calculate_repetition_penalty(password):
    char_counts = Counter(password)
    
    penalty = 0
    for char, count in char_counts.items():
        if count > 3:
            penalty += (count - 3)
    
    return min(penalty, len(password) // 2)

def calculate_dictionary_penalty(password):

    with open("10k-most-common.txt", 'r') as file:
            most_common_passwords = file.read().splitlines()
    for common_password in most_common_passwords:
        if common_password == password:
            return -1

    substitutions = {
        '@': 'a',
        '4': 'a',
        '3': 'e',
        '!': 'i',
        '1': 'l',
        '0': 'o',
        '$': 's',
        '5': 's',
        '7': 't'
    }

    normalized_password = ''.join(substitutions.get(char, char) for char in password.lower())
    filepath = "words_alpha.txt"
    penalty = 0

    with open(filepath, 'r') as file:
        dictionary_words = file.read().splitlines()

    if password.lower() in dictionary_words:
        return -1

    if normalized_password in dictionary_words:
        penalty += 20
        return penalty

    for word in dictionary_words:
        if len(word) > 3:
            if word in password.lower():
                penalty += 10
            elif word in normalized_password:
                if len(word) < len(password) // 2:
                    penalty += 3
                else:
                    penalty += 8
    return min(penalty, 30)


def calculate_pattern_penalty(password):
    penalty = 0

    # Detect repeating sequences
    if any(password[i:i + len(password)//2] * 2 == password for i in range(len(password)//2)):
        penalty += 1

    # Detect keyboard patterns
    keyboard_patterns = ["qwerty", "asdf", "zxcv", "1234", "5678", "0987"]
    for pattern in keyboard_patterns:
        if pattern in password.lower():
            penalty += 1

    # Detect sequential characters
    def is_sequential(s):
        return all(ord(s[i]) + 1 == ord(s[i + 1]) for i in range(len(s) - 1))

    if is_sequential(password) or is_sequential(password[::-1]):
        penalty += 1

    # Detect mirrored structures
    if password == password[::-1]:
        penalty += 1

    return min(penalty,5)

def calculate_entropy(password):

    # Pattern penalty
    P = calculate_pattern_penalty(password)
    # Dictionary penalty
    D = calculate_dictionary_penalty(password)
    # Repitition penalty
    R = calculate_repetition_penalty(password)

    lower_case = string.ascii_lowercase
    upper_case = string.ascii_uppercase
    digits = string.digits
    special_characters = string.punctuation

    char_set = set(password)
    possible_chars = set()

    if any(c in lower_case for c in char_set):
        possible_chars.update(lower_case)
    if any(c in upper_case for c in char_set):
        possible_chars.update(upper_case)
    if any(c in digits for c in char_set):
        possible_chars.update(digits)
    if any(c in special_characters for c in char_set):
        possible_chars.update(special_characters)
    N = len(possible_chars)
    L = len(password)

    base_entropy = L * np.log2(N)

    adjusted_length = max(1, L - P - R)
    improved_entropy = max(0,adjusted_length * np.log2(N) - D)

    if (D == -1):
        improved_entropy = 0
    

    return base_entropy, improved_entropy