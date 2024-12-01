import tkinter as tk
from tkinter import messagebox
from analyze import calculate_entropy

def analyze_password():
    password = password_entry.get()
    if not password:
        messagebox.showerror("Input Error", "Please enter a password to analyze.")
        return

    try:
        entropy = calculate_entropy(password)

        if entropy < 30:
            strength = "Weak"
            color = "red"
        elif entropy < 75:
            strength = "Moderate"
            color = "orange"
        else:
            strength = "Strong"
            color = "green"

        result_label.config(text=f"Entropy: {entropy:.2f}", fg=color)
        strength_label.config(text=f"Strength: {strength}", fg=color)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

root = tk.Tk()
root.title("Password Strength Analyzer")

window_width = 400
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_x = (screen_width // 2) - (window_width // 2)
position_y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

password_label = tk.Label(root, text="Enter Password:", font=("Helvetica", 12))
password_label.pack(pady=10)

password_entry = tk.Entry(root, width=30, font=("Helvetica", 12), show="*")
password_entry.pack(pady=5)

analyze_button = tk.Button(root, text="Analyze Password", font=("Helvetica", 12), command=analyze_password)
analyze_button.pack(pady=15)

result_label = tk.Label(root, text="", font=("Helvetica", 14))
result_label.pack(pady=5)

strength_label = tk.Label(root, text="", font=("Helvetica", 14))
strength_label.pack(pady=5)

root.mainloop()
