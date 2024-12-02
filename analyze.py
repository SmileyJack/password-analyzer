import numpy as np
import string
from collections import Counter

def analyze_password_file(file_path):

    sorted_dict = {}
    try:
        with open(file_path, 'r') as file:
            passwords = file.read().splitlines()
        
        print(f"Total passwords in file: {len(passwords)}")

        # weak_passwords = [pwd.strip() for pwd in passwords if len(pwd.strip()) < 8]
        # print(f"Weak passwords (less than 8 characters): {len(weak_passwords)}")

        identify_common_passwords(passwords)

        pass_dict = {}
        for password in passwords:
            entropy, improved = calculate_entropy(password)
            pass_dict[password] = entropy

        sorted_dict = dict(sorted(pass_dict.items(), key=lambda item: item[1], reverse=True))

        
    except FileNotFoundError:
        print("The file was not found. Please check the file path and try again.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return sorted_dict

def identify_common_passwords(passwords):

    with open("10k-most-common.txt", 'r') as file:
            most_common_passwords = file.read().splitlines()

    for password in passwords:
        for common_password in most_common_passwords:
            if common_password == password:
                print("password that is too common was found: " + password)

def calculate_repetition_penalty(password):
    char_counts = Counter(password)
    
    penalty = 0
    for char, count in char_counts.items():
        if count > 3:
            penalty += (count - 3)
    
    return penalty

def calculate_dictionary_penalty(password):
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
        penalty += 30

    for word in dictionary_words:
        if len(word) > 3:
            if word in password.lower():
                penalty += 20
            elif word in normalized_password:
                penalty += 15
    return penalty


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

    return penalty

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

    improved_entropy = (L - P - R) * np.log2(N) - D

    if (D == -1):
        improved_entropy = 0
    

    return base_entropy, improved_entropy

def display_results(sorted_passwords):
        # Sort the dictionary by entropy values in descending order
    sorted_passwords = sorted(sorted_passwords.items(), key=lambda item: item[1], reverse=True)
    
    # Print the header
    print("PASSWORDS RANKED BY ENTROPY")
    
    # Display each password and its entropy value
    for rank, (password, entropy) in enumerate(sorted_passwords, start=1):
        print(f"{rank}. {password}: {entropy:.3f}")


def main():
    # file_path = input("Please enter the path to the file containing the passwords: ")
    file_path = "passwords.txt"
    sorted_passwords = analyze_password_file(file_path)
    display_results(sorted_passwords)

if __name__ == "__main__":
    main()
