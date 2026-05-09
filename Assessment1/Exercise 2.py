import tkinter as tk
from tkinter import messagebox
import random
import os

class AdvancedAlexaJokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa's Comedy Hour")
        self.root.geometry("550x500")
        self.root.configure(bg="#2c3e50") # Modern dark theme start
        
        # New Jokes to add to your collection
        self.extra_jokes = [
            "Why don't scientists trust atoms?Because they make up everything.",
            "What do you call a fake noodle?An impasta.",
            "Why did the scarecrow win an award?Because he was outstanding in his field.",
            "How does a penguin build its house?Igloos it together.",
            "What do you call a bear with no teeth?A gummy bear.",
            "Why was the math book sad?Because it had too many problems."
        ]
        
        self.jokes = self.load_and_sync_jokes()
        self.count = 0
        
        # --- UI Elements ---
        self.setup_label = tk.Label(root, text="Ready for a laugh?", font=("Segoe UI", 14, "bold"), 
                                    wraplength=450, bg="#2c3e50", fg="#ecf0f1")
        self.setup_label.pack(pady=(40, 10))

        self.punch_label = tk.Label(root, text="", font=("Segoe UI", 13, "italic"), 
                                    fg="#f1c40f", bg="#2c3e50", wraplength=450)
        self.punch_label.pack(pady=10)

        # Creative Extra: Reaction/Laugh Label
        self.reaction_label = tk.Label(root, text="", font=("Arial", 10, "bold"), bg="#2c3e50", fg="#2ecc71")
        self.reaction_label.pack(pady=5)

        # --- Button Styling ---
        btn_config = {"font": ("Arial", 10, "bold"), "width": 20, "pady": 5}
        
        self.joke_btn = tk.Button(root, text="Alexa, tell me a Joke", command=self.get_new_joke, 
                                  bg="#3498db", fg="white", **btn_config)
        self.joke_btn.pack(pady=5)

        self.punch_btn = tk.Button(root, text="Show Punchline", command=self.reveal_punchline, 
                                   state="disabled", bg="#95a5a6", fg="white", **btn_config)
        self.punch_btn.pack(pady=5)

        # Creative Extra: Copy Joke Button
        self.copy_btn = tk.Button(root, text="📋 Copy Joke", command=self.copy_to_clipboard, 
                                  bg="#34495e", fg="white", width=15)
        self.copy_btn.pack(pady=10)

        self.quit_btn = tk.Button(root, text="Exit", command=root.quit, bg="#e74c3c", fg="white")
        self.quit_btn.pack(side="bottom", pady=20)

    def load_and_sync_jokes(self):
        """Loads jokes from file and adds the new ones if they aren't there."""
        file_path = "randomJokes.txt"
        existing_jokes = []

        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                existing_jokes = [line.strip() for line in f if line.strip()]

        # Merge with extra jokes, avoiding duplicates
        combined = list(set(existing_jokes + self.extra_jokes))
        
        # Save them back to the file so they are permanent
        with open(file_path, "w") as f:
            for joke in combined:
                f.write(joke + "\n")
        
        return combined

    def get_new_joke(self):
        full_joke = random.choice(self.jokes)
        if "?" in full_joke:
            parts = full_joke.split("?", 1)
            self.current_setup = parts[0] + "?"
            self.current_punchline = parts[1].strip()
        else:
            self.current_setup = "Here's a quick one..."
            self.current_punchline = full_joke

        self.setup_label.config(text=self.current_setup)
        self.punch_label.config(text="")
        self.reaction_label.config(text="") # Reset reaction
        self.punch_btn.config(state="normal", bg="#f39c12")
        
        # Smoothly transition background color
        self.update_theme()

    def reveal_punchline(self):
        self.punch_label.config(text=self.current_punchline)
        self.punch_btn.config(state="disabled", bg="#95a5a6")
        self.trigger_laugh_track()

    def trigger_laugh_track(self):
        """Extra Function: Simulates an audience reaction."""
        reactions = ["*Laughter Intensifies*", "😂 Hahaha!", "Ba-dum Tss! 🥁", "Oh, Alexa... 🙄", "Classic!"]
        self.reaction_label.config(text=random.choice(reactions))

    def copy_to_clipboard(self):
        """Extra Function: Copies the current joke to the system clipboard."""
        if hasattr(self, 'current_setup') and self.punch_label.cget("text"):
            joke_text = f"{self.current_setup} {self.current_punchline}"
            self.root.clipboard_clear()
            self.root.clipboard_append(joke_text)
            messagebox.showinfo("Copied", "Joke copied to clipboard!")
        else:
            messagebox.showwarning("Wait", "Reveal the punchline before copying!")

    def update_theme(self):
        """Changes the window accent colors randomly."""
        colors = ["#1abc9c", "#9b59b6", "#34495e", "#16a085", "#2c3e50"]
        new_color = random.choice(colors)
        self.root.config(bg=new_color)
        self.setup_label.config(bg=new_color)
        self.punch_label.config(bg=new_color)
        self.reaction_label.config(bg=new_color)

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedAlexaJokeApp(root)
    root.mainloop()