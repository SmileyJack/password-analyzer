import numpy as np
import string
from collections import Counter
from entropy import calculate_entropy

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

def display_results(sorted_passwords):
        # Sort the dictionary by entropy values in descending order
    sorted_passwords = sorted(sorted_passwords.items(), key=lambda item: item[1], reverse=True)
    # Print the header
    print("PASSWORDS RANKED BY ENTROPY")
    
    # Display each password and its entropy value
    for rank, (password, entropy) in enumerate(sorted_passwords, start=1):
        print(f"{rank}. {password}: {entropy:.3f}")

def visualize_entropy(entropies):
    passwords = [item[0] for item in entropies]
    base_entropies = [item[1] for item in entropies]
    improved_entropies = [item[2] for item in entropies]

    x = np.arange(len(passwords))
    width = 0.35

    plt.figure(figsize=(10, 6))
    plt.bar(x - width / 2, base_entropies, width, label="Base Entropy", alpha=0.8)
    plt.bar(x + width / 2, improved_entropies, width, label="Improved Entropy", alpha=0.8)

    plt.xlabel("Passwords")
    plt.ylabel("Entropy")
    plt.title("Password Entropy Comparison")
    plt.xticks(x, passwords, rotation=45, ha="right")
    plt.legend()

    plt.tight_layout()
    plt.show()


def main():
    # file_path = input("Please enter the path to the file containing the passwords: ")
    file_path = "passwords.txt"
    sorted_passwords = analyze_password_file(file_path)
    display_results(sorted_passwords)

if __name__ == "__main__":
    main()
