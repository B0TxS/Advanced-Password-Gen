import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Password Generator")
        self.root.geometry("500x480")
        self.root.configure(bg="#121212")
        self.root.resizable(False, False)

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")

        style.configure("TFrame", background="#121212")
        style.configure("TLabel", background="#121212", foreground="#ffffff", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI Semibold", 18), foreground="#00e0ff", background="#121212")
        style.configure("TCheckbutton", background="#121212", foreground="#cccccc")
        style.configure("TButton", background="#1f1f1f", foreground="#ffffff", font=("Segoe UI", 10), padding=6, relief="flat")
        style.map("TButton",
                  background=[("active", "#2a2a2a")],
                  foreground=[("disabled", "#666666")])

    def create_widgets(self):
        ttk.Label(self.root, text="Advanced Password Generator", style="Header.TLabel").pack(pady=(20, 5))

        options_frame = ttk.Frame(self.root)
        options_frame.pack(pady=10)

        ttk.Label(options_frame, text="Password Length:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.length_var = tk.IntVar(value=16)
        self.length_entry = tk.Entry(options_frame, textvariable=self.length_var, width=8,
                                     font=("Segoe UI", 10), bg="#1e1e1e", fg="#ffffff", insertbackground="white")
        self.length_entry.grid(row=0, column=1, padx=5, pady=5)

        self.lower_var = tk.BooleanVar(value=True)
        self.upper_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.special_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(options_frame, text="Include lowercase (a-z)", variable=self.lower_var).grid(row=1, column=0, columnspan=2, sticky='w', padx=5)
        ttk.Checkbutton(options_frame, text="Include uppercase (A-Z)", variable=self.upper_var).grid(row=2, column=0, columnspan=2, sticky='w', padx=5)
        ttk.Checkbutton(options_frame, text="Include numbers (0-9)", variable=self.digits_var).grid(row=3, column=0, columnspan=2, sticky='w', padx=5)
        ttk.Checkbutton(options_frame, text="Include symbols (!@#$%^&*)", variable=self.special_var).grid(row=4, column=0, columnspan=2, sticky='w', padx=5)

        ttk.Label(self.root, text="Generated Password:", font=("Segoe UI Semibold", 12)).pack(pady=(20, 5))

        self.password_entry = tk.Entry(self.root, font=("Consolas", 14), width=34, justify="center",
                                       bg="#1e1e1e", fg="#00ffcc", insertbackground="white", relief="flat", bd=2)
        self.password_entry.pack(pady=5)

        self.strength_label = ttk.Label(self.root, text="Strength: N/A", font=("Segoe UI", 10))
        self.strength_label.pack(pady=(0, 10))

        buttons_frame = ttk.Frame(self.root)
        buttons_frame.pack(pady=10)

        ttk.Button(buttons_frame, text="🔄 Generate", command=self.generate_password).grid(row=0, column=0, padx=15)
        ttk.Button(buttons_frame, text="📋 Copy", command=self.copy_password).grid(row=0, column=1, padx=15)


    def generate_password(self):
        length = self.length_var.get()
        if length < 4:
            messagebox.showwarning("Warning", "Password length must be at least 4 characters.")
            return

        charset = ""
        if self.lower_var.get(): charset += string.ascii_lowercase
        if self.upper_var.get(): charset += string.ascii_uppercase
        if self.digits_var.get(): charset += string.digits
        if self.special_var.get(): charset += string.punctuation

        if not charset:
            messagebox.showerror("Error", "Please select at least one character type.")
            return

        password = ''.join(random.choice(charset) for _ in range(length))
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        self.update_strength(password)

    def copy_password(self):
        password = self.password_entry.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Copied", "Password copied to clipboard!")

    def update_strength(self, password):
        score = sum([
            any(c.islower() for c in password),
            any(c.isupper() for c in password),
            any(c.isdigit() for c in password),
            any(c in string.punctuation for c in password),
            len(password) >= 12
        ])

        levels = {
            1: "Very Weak ",
            2: "Weak ",
            3: "Moderate ",
            4: "Strong!",
            5: "Very Strong!!!",
        }
        self.strength_label.config(text=f"Strength: {levels.get(score, 'N/A')}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
