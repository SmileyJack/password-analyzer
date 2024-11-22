import numpy as np
import string

def analyze_password_file(file_path):
    try:
        with open(file_path, 'r') as file:
            passwords = file.readlines()
        
        print(f"Total passwords in file: {len(passwords)}")

        weak_passwords = [pwd.strip() for pwd in passwords if len(pwd.strip()) < 8]
        print(f"Weak passwords (less than 8 characters): {len(weak_passwords)}")

        pass_dict = {}
        for password in passwords:
            entropy = calculate_entropy(password)
            new_pass = "\n".join(line.strip() for line in password.splitlines()) # strips new lines so we dont have to deal with it
            pass_dict[new_pass] = entropy

        sorted_dict = dict(sorted(pass_dict.items(), key=lambda item: item[1], reverse=True))

        # print(sorted_dict)
        # print(pass_dict)
        
    except FileNotFoundError:
        print("The file was not found. Please check the file path and try again.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return sorted_dict


def calculate_entropy(password):
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

    entropy = L * np.log2(N)
    return entropy

def display_results(sorted_passwords):
        # Sort the dictionary by entropy values in descending order
    sorted_passwords = sorted(sorted_passwords.items(), key=lambda item: item[1], reverse=True)
    
    # Print the header
    print("PASSWORDS RANKED BY ENTROPY")
    
    # Display each password and its entropy value
    for rank, (password, entropy) in enumerate(sorted_passwords, start=1):
        print(f"{rank}. {password}: {entropy:.3f}")


def main():
    file_path = input("Please enter the path to the file containing the passwords: ")
    sorted_passwords = analyze_password_file(file_path)
    display_results(sorted_passwords)

if __name__ == "__main__":
    main()
