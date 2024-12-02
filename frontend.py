import tkinter as tk
from tkinter import messagebox
from entropy import calculate_entropy

def analyze_password():
    password = password_entry.get()
    if not password:
        messagebox.showerror("Input Error", "Please enter a password to analyze.")
        return

    try:
        base_entropy, improved_entropy = calculate_entropy(password)

        if base_entropy < 40:
            base_strength = "Weak"
            base_color = "red"
        elif base_entropy < 75:
            base_strength = "Moderate"
            base_color = "orange"
        elif base_entropy < 100:
            base_strength = "Strong"
            base_color = "green"
        elif base_entropy < 150:
            base_strength = "Very Strong"
            base_color = "green"
        else:
            base_strength = "UNHACKABLE"
            base_color = "green"

        if improved_entropy < 40:
            improved_strength = "Weak"
            improved_color = "red"
        elif improved_entropy < 75:
            improved_strength = "Moderate"
            improved_color = "orange"
        elif improved_entropy < 100:
            improved_strength = "Strong"
            improved_color = "green"
        elif improved_entropy < 150:
            improved_strength = "Very Strong"
            improved_color = "green"
        else:
            improved_strength = "UNHACKABLE"
            improved_color = "green"

        base_entropy_label.config(text=f"Base Entropy: {base_entropy:.2f}", fg=base_color)
        base_strength_label.config(text=f"Base Strength: {base_strength}", fg=base_color)

        improved_entropy_label.config(text=f"Improved Entropy: {improved_entropy:.2f}", fg=improved_color)
        improved_strength_label.config(text=f"Improved Strength: {improved_strength}", fg=improved_color)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

root = tk.Tk()
root.title("Password Strength Analyzer")

window_width = 500
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_x = (screen_width // 2) - (window_width // 2)
position_y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

title_label = tk.Label(root, text="Password Strength Analyzer", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

input_frame = tk.Frame(root, padx=10, pady=10)
input_frame.pack(fill="x")

password_label = tk.Label(input_frame, text="Enter Password:", font=("Helvetica", 12))
password_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

password_entry = tk.Entry(input_frame, width=30, font=("Helvetica", 12))
password_entry.grid(row=0, column=1, padx=5, pady=5)

analyze_button = tk.Button(input_frame, text="Analyze Password", font=("Helvetica", 12), command=analyze_password)
analyze_button.grid(row=0, column=2, padx=5, pady=5)

results_frame = tk.Frame(root, padx=10, pady=10)
results_frame.pack(fill="x")

base_frame = tk.LabelFrame(results_frame, text="Base Entropy", font=("Helvetica", 12, "bold"), padx=10, pady=10)
base_frame.pack(fill="x", padx=10, pady=5)

base_entropy_label = tk.Label(base_frame, text="", font=("Helvetica", 14))
base_entropy_label.pack(pady=5)

base_strength_label = tk.Label(base_frame, text="", font=("Helvetica", 14))
base_strength_label.pack(pady=5)

improved_frame = tk.LabelFrame(results_frame, text="Improved Entropy", font=("Helvetica", 12, "bold"), padx=10, pady=10)
improved_frame.pack(fill="x", padx=10, pady=5)

improved_entropy_label = tk.Label(improved_frame, text="", font=("Helvetica", 14))
improved_entropy_label.pack(pady=5)

improved_strength_label = tk.Label(improved_frame, text="", font=("Helvetica", 14))
improved_strength_label.pack(pady=5)

root.mainloop()
